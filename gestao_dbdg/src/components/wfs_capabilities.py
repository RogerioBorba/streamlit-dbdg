from gestao_dbdg.src.capabilities.wfs_get_capabilities import WFSCapabilities
from gestao_dbdg.src.wfs.wfs_layer import WFSLayer
from gestao_dbdg.src.wfs.decribe_feature_type import WFSDescribeFeatureType
import streamlit as st
import asyncio

async def create_column(url: str)-> None:
    sigla: str = url[8:].split('/')[0]
    wms_capabilities = WFSCapabilities(url, sigla, url)
    for col in st.columns(1):
        await create_column_content(col, wms_capabilities)


def layer_column_content(container, layer: WFSCapabilities):
    with container:
        
        st.caption(f"Nome: :green[{layer.simple_name()}]")
        st.markdown(f":gray[Título:] {layer.title()}")
        st.markdown(f":gray[Resumo:] {layer.abstract() or 'Não há resumo'}")
        st.markdown(f":gray[Palavras-chaves:] {','.join(layer.palavras_chaves()) or 'sem palavras-chaves'}")
        st.markdown(f":gray[CRSs:] {','.join(layer.crss())}")
        if layer.metadados_urls:
            for metadata_url in layer.metadados_urls:
                md = ":gray[Metadado:] [link](%s)  tipo: %s" % (metadata_url.url, metadata_url.type)
                st.markdown(md)
        else:
            st.markdown(':gray[Metadado:] Sem link')
        #print(layer.url_metadado_links())
    return container

def create_layers_columns(layers: list[WFSLayer]) -> None:
    size_of_layers = len(layers)
    iterator = size_of_layers// 3 + ( 0 if size_of_layers % 3 == 0  else 1)
    idx_layers: int = 0
    for i in range(iterator):
        for col in st.columns(3):
            if idx_layers < size_of_layers:
                layer: WFSLayer = layers[idx_layers]
                layer_column_content(col, layer)
                idx_layers += 1


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
        st.text(f"Qtd de camadas: {capabilities.qtd_camadas}")
        st.text(f"Qtd sem metadados: {capabilities.qtd_camadas_sem_metadados}")
        st.text(f"Qtd sem palavras chaves: {capabilities.qtd_camadas_sem_palavras_chaves}")
        st.text(f"Qtd sem resumo: {capabilities.qtd_camadas_sem_resumo}")
        if  not capabilities.failed:
            st.button("Detalhe", key=capabilities.descricao, on_click= create_layers_columns, args=[capabilities.layers()])
            st.session_state['wfs_capability'] = capabilities
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
                idx_capabilities += 1
    await asyncio.gather(*tasks)


