import asyncio
from collections import namedtuple
from io import StringIO
from gestao_dbdg.src.inde_dbdg.inde import wfs_capabilities
from gestao_dbdg.src.capabilities.wfs_get_capabilities import WFSCapabilities
from gestao_dbdg.src.wfs.wfs_layer import WFSLayer
import streamlit as st
from lxml import etree
import requests
import pandas as pd

HEADER_TIPO_FEICAO: str = 'nome_feicao;atributo;tipo;multiplicidade'


def get_xml(url: str) -> str:
    session = requests.Session()
    session.verify = False
    with session:
        res = requests.get(url)
        return res.text


def element_list(xml: str, path: str = '') -> list:
    xml_encoded: bytes = xml.encode()
    # Parse XML content
    root = etree.fromstring(xml_encoded)
    # get its namespace map, excluding default namespace
    nsmap = ns_map(root)
    # Iterate over complex types
    return root.findall(path, namespaces=nsmap)


def lista_complex_type(xml: str) -> list:
    complex_type_list: list = element_list(xml, './/xsd:complexType')
    return complex_type_list


def describe_complex_type(container, complex_type, nsmap):
    with container:
        type_name = complex_type.get('name')
        tipo_fei: str = f'Nome: {type_name[:-4]}'
        st.markdown(f'<h6> {tipo_fei} </h6>', unsafe_allow_html=True)
        # Count attributes
        attributes = complex_type.findall('.//xsd:element', namespaces=nsmap)
        num_attributes = len(attributes)
        st.text(f'Quantidade de atributos: {num_attributes}')
        # Display attribute details
        for attribute in attributes:
            attr_name = attribute.get('name')
            attr_type = attribute.get('type')
            st.text(f'{attr_name} : {attr_type[4:]}[{attribute.get("minOccurs")}..{attribute.get("maxOccurs")}]')
        st.text('')


def complex_type_as_csv_string(complex_type, nsmap) -> str:
    csv_data: str = ''
    attributes = complex_type.findall('.//xsd:element', namespaces=nsmap)
    for attribute in attributes:
        attr_name = attribute.get('name')
        attr_type = attribute.get('type')
        csv_data += f'{complex_type.get("name")[:-4]};{attr_name};{attr_type[4:]};{attribute.get("minOccurs")}..{attribute.get("maxOccurs")}\n'
    return csv_data


def ns_map(root):
    return {k: v for k, v in root.nsmap.items() if k}


def complex_type_as_list(xml_content: str):
    complex_type_list = lista_complex_type(xml_content)
    size_of_complex_type_list = len(complex_type_list)
    if size_of_complex_type_list == 0:
        lista = element_list(xml_content, './/xsd:import')
        for ele in lista:
            if 'schemaLocation' in ele.attrib:
                xml: str = get_xml(ele.attrib['schemaLocation'])
                complex_type_list.extend(lista_complex_type(xml))
    return complex_type_list


def describe_feature_type(xml_content: str):
    complex_type_list = complex_type_as_list(xml_content)
    size_of_complex_type_list = len(complex_type_list)
    iterator = size_of_complex_type_list // 3 + (0 if size_of_complex_type_list % 3 == 0 else 1)
    idx_complex_type: int = 0
    root = etree.fromstring(xml_content.encode())
    nsmap = ns_map(root)
    for i in range(iterator):
        for col in st.columns(3):
            if idx_complex_type < size_of_complex_type_list:
                complex_type = complex_type_list[idx_complex_type]
                describe_complex_type(col, complex_type, nsmap)
                idx_complex_type += 1
    

def describe_feature_type_as_csv(xml_content: str) -> str:
    complex_type_list = complex_type_as_list(xml_content)
    root = etree.fromstring(xml_content.encode())
    nsmap = ns_map(root)
    cvs_content: str = ''
    for complex_type in complex_type_list:
        linha: str = complex_type_as_csv_string(complex_type, nsmap)
        cvs_content += linha
    return cvs_content


def url_describe(url: str, layers: list[WFSLayer] | None = None) -> str | None:
    url_begin: str = url[0:url.index('?')]
    if layers:
        type_names: str = ','.join([layer.name() for layer in layers])
        url = f'{url_begin}?service=wfs&version=2.0.0&request=DescribeFeatureType&typeNames={type_names}'
        encoded_url = requests.utils.requote_uri(url)
        return encoded_url
    return None


def create_sublists(input_list: list, max_elements: int = 100):
    sublists: list = [input_list[i:i + max_elements] for i in range(0, len(input_list), max_elements)]
    return sublists


def layer_detail(capabilities):    
    sub_listas: list[list] = create_sublists(capabilities.layers())
    for lista in sub_listas:
        session = requests.Session()
        session.verify = False
        with session:
            iri = url_describe(capabilities.url, lista)
            xml: str = get_xml(iri)
            describe_feature_type(xml)


def csv_view(capabilities):
    sub_listas: list[list] = create_sublists(capabilities.layers())
    csv_file_content: str = f'{HEADER_TIPO_FEICAO}\n'
    for lista in sub_listas:
        session = requests.Session()
        session.verify = False
        with session:
            iri = url_describe(capabilities.url, lista)
            csv_file_content += describe_feature_type_as_csv(get_xml(iri))
    content = StringIO(csv_file_content)
    df = pd.read_csv(content, sep=';')
    st.dataframe(df, use_container_width=True)  # Same as st.write(df)


def layer_csv(capabilities):
    sub_listas: list[list] = create_sublists(capabilities.layers())
    csv_file_content: str = f'{HEADER_TIPO_FEICAO}\n'
    for lista in sub_listas:
        session = requests.Session()
        session.verify = False
        with session:
            iri = url_describe(capabilities.url, lista)
            csv_file_content += describe_feature_type_as_csv(get_xml(iri))
    st.session_state.csv_content = csv_file_content


async def create_column_content(container, capabilities):
    try:        
        await capabilities.execute_request()
    except Exception as exc:
        print(exc)
        capabilities.failed = True
    with container:      
        if capabilities.failed:
            st.caption(f"{capabilities.descricao} :red[Requisição Falhou!]")
        else:
            st.caption(capabilities.descricao)
        st.text(f"Tempo de requisicão: {capabilities.tempo_requisicao}")
        st.text(f"Qtd de tipo de feições: {capabilities.qtd_camadas}")
        if capabilities.failed:
            return
        col1, col2 = st.columns(2)
        with col1:
            st.button("Detalhe", key=capabilities.descricao, on_click=layer_detail, args=[capabilities])
        with col2:
            st.button("CSV", key=f'{capabilities.descricao}_csv', on_click=csv_view, args=[capabilities])
    return container


async def create_columns(l_capabilities: list[WFSCapabilities]) -> None:
    size_of_capabilities = len(l_capabilities)
    iterator = size_of_capabilities // 3 + (0 if size_of_capabilities % 3 == 0 else 1)
    idx_capabilities: int = 0
    tasks = []
    for i in range(iterator):
        for col in st.columns(3):
            if idx_capabilities < size_of_capabilities:
                capabilities = l_capabilities[idx_capabilities]
                col.key = capabilities.descricao
                task = asyncio.create_task(create_column_content(col, capabilities))
                tasks.append(task) 
                idx_capabilities += 1
    await asyncio.gather(*tasks)


async def main():
    st.set_page_config(page_title="WFS - Tipos de feição", page_icon="👋", layout="wide")
    descricoes_escolhidas = []
    list_descricao_sigla_url: list[namedtuple] = await wfs_capabilities()
    descricoes: list[str] = [descricao_sigla_url.descricao for descricao_sigla_url in list_descricao_sigla_url]
    selecionar_todas = st.sidebar.checkbox('Selecionar todas instituições')
    if selecionar_todas:
        descricoes_escolhidas = descricoes
    options = st.sidebar.multiselect('-----', descricoes, descricoes_escolhidas)
    url_preenchida = st.sidebar.text_input("Ou informe um URL")
    btn = st.sidebar.button('Executar')
    capabilities: list[WFSCapabilities] = []
    if btn:
        if url_preenchida:
            pass  # await create_column(url_preenchida)
        else:
            capabilities = [WFSCapabilities(descricao, sigla, url) for descricao, sigla, url
                            in list_descricao_sigla_url if descricao in options]
        await create_columns(capabilities)

asyncio.run(main())
