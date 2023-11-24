import asyncio
import streamlit as st
from src.wms_get_capabilities import WMSCapabilities
from collections import namedtuple
from src.inde import wms_capabilities, qtd_camadas_sem_metadados, qtd_camadas, falhas, qtd_catalogos, incremento_catalogos
#print(qtd_camadas_sem_metadados)
#print(qtd_camadas)
def container_content(container, descricao = ''):
    with container:
        st.progress(qtd_catalogos, descricao)
        st.caption(f"Total de camadas: :green[{qtd_camadas}]")
        st.caption(f"Total de camadas sem metadados: :red[{qtd_camadas_sem_metadados}]")
        st.caption(f"Falhas em: :red[{falhas}]")
        

async def summary_wms_capabilities(placeholder, wms_capabilities: WMSCapabilities):
    global qtd_camadas
    global qtd_camadas_sem_metadados
    global falhas
    global incremento_catalogos
    global qtd_catalogos
    
    qtd_catalogos += incremento_catalogos
    try:
        await wms_capabilities.execute_request()
        qtd_camadas += wms_capabilities.qtd_camadas
        qtd_camadas_sem_metadados += wms_capabilities.qtd_camadas_sem_metadados
        if qtd_catalogos > 1.0:
            qtd_catalogos = 1.0

    except Exception as exc:
        print(wms_capabilities.descricao)
        print(exc)
        falhas.append(wms_capabilities.descricao)
    finally:
        placeholder.empty()
        container = placeholder.container()
        container_content(container, wms_capabilities.descricao)
        print(qtd_catalogos)


async def create_content(lista_descricao_sigla_url: list[tuple[str,str]], descricoes_escolhidas: list[str])-> None:
    l_descricao_sigla_url : list[tuple[str, str,str]] = [ (descricao, sigla, url) for descricao, sigla, url in lista_descricao_sigla_url if descricao in descricoes_escolhidas]
    l_wms_get_capabilities: list[WMSCapabilities] = [ WMSCapabilities(descricao, sigla, url) for descricao, sigla, url in l_descricao_sigla_url]
    tasks: list = []
    global qtd_camadas
    global qtd_camadas_sem_metadados
    global falhas
    global incremento_catalogos
    falhas = []
    incremento_catalogos = round(1/len(l_wms_get_capabilities), 2)

    placeholder = st.empty()
    container = placeholder.container()
    container_content(container)
    for wms_capabilities in l_wms_get_capabilities:
        task = asyncio.create_task(summary_wms_capabilities(placeholder, wms_capabilities))
        tasks.append(task)    
    await asyncio.gather(*tasks)
    

async def main():
    st.set_page_config( page_title="WMS - Sumário de Catálogos", page_icon="👋", layout="wide" )
    descricoes_escolhidas = []
    list_descricao_sigla_url: list[namedtuple] = await wms_capabilities()
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