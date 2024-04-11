import asyncio
import streamlit as st
from gestao_dbdg.src.capabilities.wms_get_capabilities import WMSCapabilities
from collections import namedtuple
from gestao_dbdg.src.inde_dbdg.inde import wms_capabilities_catalogo_inde
#print(qtd_camadas_sem_metadados)
#print(qtd_camadas)
def container_content(container, wms_capa = None):
    with container:
        descricao = wms_capa.descricao if wms_capa else ''
        st.text(f"Total de camadas processadas por selecionadas {st.session_state.qtd_total_catalogos_processados}/{st.session_state.qtd_total_catalogos_selecionados}")
        st.progress(st.session_state.qtd_catalogos, descricao)
        st.caption(f"Total de camadas: :green[{st.session_state.qtd_camadas}]")
        st.caption(f"Total de camadas sem metadados: :red[{st.session_state.qtd_camadas_sem_metadados}]")
        st.caption(f"Total de camadas sem resumo: :red[{st.session_state.qtd_camadas_sem_resumo}]")
        st.caption(f"Falhas em: :red[{st.session_state.falhas}]")
        

async def summary_wms_capabilities(placeholder, wms_capabilities_catalogo_inde: WMSCapabilities):
    
    try:
        await wms_capabilities.execute_request()
        st.session_state.qtd_camadas += wms_capabilities.qtd_camadas
        st.session_state.qtd_camadas_sem_metadados += wms_capabilities.qtd_camadas_sem_metadados
        st.session_state.qtd_camadas_sem_resumo += wms_capabilities.qtd_camadas_sem_resumo

    except Exception as exc:
        st.session_state.qtd_catalogos += st.session_state.incremento_catalogos
        print(f"falha em: {wms_capabilities.descricao}")
        print(f"falha: {exc}")
        wms_capabilities.failed = True
        st.session_state.falhas.append(wms_capabilities.descricao)
    finally:
        st.session_state.qtd_catalogos += st.session_state.incremento_catalogos
        st.session_state.qtd_total_catalogos_processados += 1
        print(f"st.session_state.qtd_total_catalogos_processados: {st.session_state.qtd_total_catalogos_processados}")
        if st.session_state.qtd_catalogos > 1.0:
            st.session_state.qtd_catalogos = 1.0
        placeholder.empty()
        container = placeholder.container()
        container_content(container, wms_capabilities)


async def create_content(lista_descricao_sigla_url: list[tuple[str,str]], descricoes_escolhidas: list[str]) -> None:

    l_wms_get_capabilities: list[WMSCapabilities] = [WMSCapabilities(descricao, sigla, url) for descricao, sigla, url in
                                                     lista_descricao_sigla_url if descricao in descricoes_escolhidas]
    tasks: list = []
    st.session_state.falhas = []
    size: int = len(l_wms_get_capabilities)
    if size ==0:
        return                 
    st.session_state.incremento_catalogos = round(1/size, 2)
    st.session_state.qtd_total_catalogos_selecionados = len(l_wms_get_capabilities)
    placeholder = st.empty()
    container = placeholder.container()
    container_content(container)
    for wms_capabilities in l_wms_get_capabilities:
        task = asyncio.create_task(summary_wms_capabilities(placeholder, wms_capabilities))
        tasks.append(task)    
    await asyncio.gather(*tasks)

    
def initialize_session():
    st.session_state.qtd_camadas = 0
    st.session_state.qtd_camadas_sem_metadados = 0
    st.session_state.falhas = []
    st.session_state.incremento_catalogos = 0.0
    st.session_state.qtd_catalogos = 0.0
    st.session_state.qtd_total_catalogos_selecionados = 0
    st.session_state.qtd_total_catalogos_processados = 0
    st.session_state.qtd_camadas_sem_resumo = 0
    
async def main():
    st.set_page_config( page_title="WMS - Sumário de Catálogos", page_icon="👋", layout="wide" )
    initialize_session()
    descricoes_escolhidas = []
    list_descricao_sigla_url: list[namedtuple] = await wms_capabilities_catalogo_inde()
    descricoes: list[str] = [descricao_sigla_url.descricao for descricao_sigla_url in list_descricao_sigla_url]
    header = st.sidebar.header("Sumário catálogos WMS")
    selecionar_todas = st.sidebar.checkbox('Selecionar todas instituições')
    if selecionar_todas:
        descricoes_escolhidas = descricoes
    options = st.sidebar.multiselect('-----', descricoes, descricoes_escolhidas)
    btn = st.sidebar.button('Executar')
    if btn:
       await create_content(list_descricao_sigla_url, options)
       
asyncio.run(main())