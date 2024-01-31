import asyncio
from collections import namedtuple
from gestao_dbdg.src.inde_dbdg.inde import wfs_capabilities
from gestao_dbdg.src.capabilities.wfs_get_capabilities import WFSCapabilities
from gestao_dbdg.src.components.wfs_capabilities import create_columns
import streamlit as st


async def main():
    st.set_page_config(page_title="WFS - Capabilities", page_icon="👋", layout="wide")
    descricoes_escolhidas: list[str] = []
    list_descricao_sigla_url: list[namedtuple] = await wfs_capabilities()
    descricoes: list[str] = [descricao_sigla_url.descricao for descricao_sigla_url in list_descricao_sigla_url]
    selecionar_todas = st.sidebar.checkbox('Selecionar todas instituições')
    if selecionar_todas:
        descricoes_escolhidas = descricoes
    options = st.sidebar.multiselect('-----', descricoes, descricoes_escolhidas)
    url_preenchida = st.sidebar.text_input("Ou informe um URL")
    btn = st.sidebar.button('Executar')
    if btn:
        l_descricao_sigla_url: list[tuple[str, str, str]] = []

        if url_preenchida:
            pass  # await create_column(url_preenchida)
        else:
            l_descricao_sigla_url = [(descricao, sigla, url) for descricao, sigla, url
                                                                 in list_descricao_sigla_url if
                                                                 descricao in options]
        l_capabilities = [WFSCapabilities(descricao, sigla, url) for descricao, sigla, url in l_descricao_sigla_url]
        await create_columns(l_capabilities)
asyncio.run(main())
