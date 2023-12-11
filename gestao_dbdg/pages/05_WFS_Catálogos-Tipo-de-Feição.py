import asyncio
from collections import namedtuple
from gestao_dbdg.src.inde_dbdg.inde import wfs_capabilities
from gestao_dbdg.src.capabilities.wfs_get_capabilities import WFSCapabilities
from gestao_dbdg.src.wfs.wfs_layer import WFSLayer
import streamlit as st
from lxml import etree
from gestao_dbdg.src.requests.request import fetch_xml
from streamlit_extras.switch_page_button import switch_page
import requests
#from urllib3.exceptions import InsecureRequestWarning
def decribe_complext_type(container, complex_type, nsmap):
    with container:
        type_name = complex_type.get('name')
        st.caption(f'Tipo da Feição: {type_name[:-4]}')
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

def describe_feature_type(xml_content: str):
    # Parse XML content
    root = etree.fromstring(xml_content)
    # get its namespace map, excluding default namespace    
    nsmap = {k:v for k,v in root.nsmap.items() if k}
    # Iterate over complex types
    complex_type_list: list = root.findall('.//xsd:complexType', namespaces=nsmap)
    size_of_complex_type_list = len(complex_type_list)
    iterator = size_of_complex_type_list // 3 + ( 0 if size_of_complex_type_list % 3 == 0  else 1)
    idx_complex_type: int = 0
    for i in range(iterator):
        for col in st.columns(3):
            if idx_complex_type < size_of_complex_type_list:
                complex_type = complex_type_list[idx_complex_type]
                decribe_complext_type(col, complex_type, nsmap)
                idx_complex_type += 1
    
        
def url_describe(url: str, layers: list[WFSLayer] | None = None) -> str | None:
     url_begin: str = url[0:url.index('?')]
     if layers:
        type_names: str = ','.join([layer.name() for layer in layers])
        #print(f'{url_begin}?service=wfs&version=2.0.0&request=DescribeFeatureType&typeNames={type_names}')
        return f'{url_begin}?service=wfs&version=2.0.0&request=DescribeFeatureType&typeNames={type_names}'
     return None


def create_sublists(input_list: list, max_elements: int = 100):
    sublists = [input_list[i:i + max_elements] for i in range(0, len(input_list), max_elements)]
    return sublists


def layer_detail(capabilities):    
    sub_listas: list[list] = create_sublists(capabilities.layers())
    for lista in sub_listas:
        url_dft: str | None = url_describe(capabilities.url, lista)  
        #requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)  
        session = requests.Session()
        session.verify = False
        with session:
            iri = url_describe(capabilities.url, lista)
            print(iri)
            res = requests.get(iri)
            xml = res.text.encode()
            describe_feature_type(xml)
    
    
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
        btn_detalhe = st.button("Detalhe", key=capabilities.descricao, on_click= layer_detail, args=[capabilities])
    return container

async def create_columns(l_capabilities: list[WFSCapabilities]) -> None:
    
    size_of_capabilities = len(l_capabilities)
    iterator = size_of_capabilities // 3 + ( 0 if size_of_capabilities % 3 == 0  else 1)
    idx_capabilities: int = 0
    tasks = []
    
    for i in range(iterator):
        for col in st.columns(3):
            if idx_capabilities < size_of_capabilities:
                capabilities = l_capabilities[idx_capabilities]
                col.key = capabilities.descricao
                task = asyncio.create_task(create_column_content(col, capabilities))
                tasks.append(task) 
                tasks.append(task)    
                idx_capabilities += 1
    await asyncio.gather(*tasks)


async def main():
    st.set_page_config( page_title="WFS - Tipos de feição", page_icon="👋", layout="wide" )
    #st.title("WMS GetCapabilities")
    descricoes_escolhidas = []
    list_descricao_sigla_url: list[namedtuple] = await wfs_capabilities()
    descricoes: list[str] = [descricao_sigla_url.descricao for descricao_sigla_url in list_descricao_sigla_url]

    header = st.sidebar.header("Instituições")
    selecionar_todas = st.sidebar.checkbox('Selecionar todas instituições')
    if selecionar_todas:
        descricoes_escolhidas = descricoes
    options = st.sidebar.multiselect('-----', descricoes, descricoes_escolhidas)
    
    url_preenchida = st.sidebar.text_input("Ou informe um URL")
    btn = st.sidebar.button('Executar')
    if btn:
            if url_preenchida:
                pass  # await create_column(url_preenchida)
            else:
                l_descricao_sigla_url: list[tuple[str, str, str]] = [(descricao, sigla, url) for descricao, sigla, url
                                                                     in list_descricao_sigla_url if
                                                                     descricao in options]
                l_capabilities = [ WFSCapabilities(descricao, sigla, url) for descricao, sigla, url in l_descricao_sigla_url]
            await create_columns(l_capabilities)
asyncio.run(main())