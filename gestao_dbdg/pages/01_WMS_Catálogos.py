import asyncio
from collections import namedtuple
import streamlit as st
from gestao_dbdg.src.inde_dbdg.inde import wms_capabilities
from streamlit_extras.switch_page_button import switch_page
from gestao_dbdg.src.capabilities.wms_get_capabilities import WMSCapabilities
from gestao_dbdg.src.wms.wms_layer import WMSLayer
from gestao_dbdg.src.requests.util_xml import  prefix_tag
wms_capability = None

def layer_column_content(container, layer: WMSLayer):
    with container:
        
        st.caption(f"Nome: :green[{layer.simple_name()}]")
        st.markdown(f":gray[Título:] {layer.title()}")
        st.markdown(f":gray[Resumo:] {layer.abstract() or 'Não há resumo'}")
        st.markdown(f":gray[Palavras-chaves:] {','.join(layer.palavras_chaves()) or 'sem palavras-chaves'}")
        st.markdown(f":gray[CRSs:] {','.join(layer.crss())}")
        st.markdown(f":gray[Estilo:] {layer.style.simple_name() if layer.style else 'sem estilo'}")
        if layer.metadados_urls:
            for metadata_url in layer.metadados_urls:
                md = ":gray[Metadado:] [link](%s)  tipo: %s" % (metadata_url.url(), metadata_url.type())
                st.markdown(md)
        else:
            st.markdown(':gray[Metadado:] Sem link')
        #print(layer.url_metadado_links())
    return container

def create_layers_columns(layers: list[WMSLayer]) -> None:
    size_of_layers = len(layers)
    iterator = size_of_layers// 3 + ( 0 if size_of_layers % 3 == 0  else 1)
    idx_layers: int = 0
    for i in range(iterator):
        for col in st.columns(3):
            if idx_layers < size_of_layers:
                layer: WMSLayer = layers[idx_layers]
                layer_column_content(col, layer)
                idx_layers += 1
        st.text("") #st.markdown("***")

def layer_detail(wms_capa):
    create_layers_columns(wms_capa.wms_layers())

async def create_column_content(container, wms_get_capabilities):
    try:
        
        await wms_get_capabilities.execute_request()
    except Exception as exc:
        print(wms_get_capabilities)
        wms_get_capabilities.failed = True
    
    with container:
        
        if wms_get_capabilities.failed:
            st.caption(f"{wms_get_capabilities.descricao} :red[Requisição Falhou!]")
        else:
            st.caption(wms_get_capabilities.descricao)
        st.text(f"Tempo de requisicão: {wms_get_capabilities.tempo_requisicao}")
        st.text(f"Qtd de camadas: {wms_get_capabilities.qtd_camadas}")
        st.text(f"Qtd sem metadados: {wms_get_capabilities.qtd_camadas_sem_metadados}")
        st.text(f"Qtd sem palavras chaves: {wms_get_capabilities.qtd_camadas_sem_palavras_chaves}")
        st.text(f"Qtd sem resumo: {wms_get_capabilities.qtd_camadas_sem_resumo}")
        #st.text(wms_get_capabilities.xml)
        if  not wms_get_capabilities.failed:
            st.button("Detalhe", key=wms_get_capabilities.descricao, on_click= layer_detail, args=[wms_get_capabilities])
            st.session_state['wms_capability'] = wms_get_capabilities
            #st.session_state['capabilities_wms'] = wms_get_capabilities
            #st.markdown('<a href="/capabilities" target="_self">Detalhes</a>', unsafe_allow_html=True)
            
    return container

async def create_column(url: str)-> None:
    sigla: str = url[8:].split('/')[0]
    wms_capabilities = WMSCapabilities(url, sigla, url)
    for col in st.columns(1):
        await create_column_content(col, wms_capabilities)


async def create_columns(lista_descricao_sigla_url: list[tuple[str,str]], descricoes_escolhidas: list[str])-> None:
    l_descricao_sigla_url : list[tuple[str, str,str]] = [ (descricao, sigla, url) for descricao, sigla, url in lista_descricao_sigla_url if descricao in descricoes_escolhidas]
    l_wms_get_capabilities = [ WMSCapabilities(descricao, sigla, url) for descricao, sigla, url in l_descricao_sigla_url]
    
    size_of_capabilities = len(l_wms_get_capabilities)
    iterator = size_of_capabilities // 3 + ( 0 if size_of_capabilities % 3 == 0  else 1)
    idx_capabilities: int = 0
    tasks = []
    
    for i in range(iterator):
        for col in st.columns(3):
            if idx_capabilities < size_of_capabilities:
                wms_get_capabilities: WMSCapabilities = l_wms_get_capabilities[idx_capabilities]
                col.key = wms_get_capabilities.descricao
                task = asyncio.create_task(create_column_content(col, wms_get_capabilities))
                tasks.append(task)    
                idx_capabilities += 1
    await asyncio.gather(*tasks)

async def main():
    st.set_page_config( page_title="WMS - Capabilities", page_icon="👋", layout="wide" )
    #st.title("WMS GetCapabilities")
    descricoes_escolhidas = []
    list_descricao_sigla_url: list[namedtuple] = await wms_capabilities()
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
            await create_column(url_preenchida)
        else:
            await create_columns(list_descricao_sigla_url, options)
asyncio.run(main())