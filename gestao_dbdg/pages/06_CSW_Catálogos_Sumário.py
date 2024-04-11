import asyncio
import time
import streamlit as st
from gestao_dbdg.src.requests.request import get_xml
from gestao_dbdg.src.requests.util_xml import hits_csw_GetRecordsResponse
from gestao_dbdg.src.inde_dbdg.csw_catalogos import csw_enderecos

def mounted_url(url_servidor: str, categoria: str | None):
    startPosition = 1
    maxRecords = 10
    url_query = f'{url_servidor}?request=GetRecords&service=CSW&version=2.0.2&typeNames=csw:Record&outputSchema=http://www.isotc211.org/2005/gmd&version=2.0.2&ElementSetName=full&resultType=hits&outputFormat=application/xml&startPosition={startPosition}&maxRecords={maxRecords}&constraintLanguage=FILTER&constraint_language_version=1.1.0'
    if categoria is None:
        return f'{url_query}'
    constraint = f'constraint=<Filter xmlns="http://www.opengis.net/ogc"><PropertyIsEqualTo><PropertyName>_cat</PropertyName><Literal>{categoria}</Literal></PropertyIsEqualTo></Filter>'
    return f'{url_query}&{constraint}'


async def create_content_to(container, dict_csw: dict):
    try:
        csw_url: str = dict_csw['cswGetCapabilities']
        url1 = csw_url[0:csw_url.index('/csw?') + 4]
        url = mounted_url(url1, dict_csw['noCentralCategoria'])
        s = time.perf_counter()
        xml = await get_xml(url, True)
        elapsed = time.perf_counter() - s
        tempo_requisicao = round(elapsed, 2)
        matched, records_returned, next_record = hits_csw_GetRecordsResponse(xml)
        with container:
            st.write(f"{dict_csw['descricao']}")
            st.write(f"tempo de requisição: {tempo_requisicao}")
            st.write(f"Qtd metadados: {matched}")
    except Exception as e:
        with container:
            st.caption(f"{dict_csw['descricao']} :red[Requisição Falhou!]")
            st.caption(f"tempo de requisição: :red[Falhou!]")
            st.caption(f"Qtd metadados:: :red[ Falhou!]")

        print(e)

async def create_columns(instituicoes_escolhidas) -> None:
    l_dic: list[dict] = [dic for dic in csw_enderecos if dic['descricao'] in instituicoes_escolhidas]
    size_of = len(l_dic)
    iterator = (size_of // 3) + (0 if size_of % 3 == 0 else 1)
    idx: int = 0
    tasks = []
    for i in range(iterator):
        for col in st.columns(3):
            if idx < size_of:
                d = l_dic[idx]
                task = asyncio.create_task(create_content_to(col, d))
                tasks.append(task)
                idx += 1
    await asyncio.gather(*tasks)


async def main():
    st.set_page_config(page_title="CSW - Sumário de Catálogos", page_icon="👋", layout="wide")
    instituicoes = [dic['descricao'] for dic in csw_enderecos]
    selecionar_todas = st.sidebar.checkbox('Selecionar todas instituições')
    instituicoes_escolhidas = []
    if selecionar_todas:
        instituicoes_escolhidas = instituicoes
    escolhidas = st.sidebar.multiselect('-----', instituicoes, instituicoes_escolhidas)
    if escolhidas:
        instituicoes_escolhidas = escolhidas
    btn = st.sidebar.button('Executar')
    if btn:
        await create_columns(instituicoes_escolhidas)


asyncio.run(main())
