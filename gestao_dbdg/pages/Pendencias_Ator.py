import asyncio
import streamlit as st
import duckdb
import pandas as pd


async def get_dataframe() -> pd.DataFrame:
    conn = duckdb.connect()
    sql: str = """
            SELECT ator.dsc_sigla, pendencia.descricao, pendencia.data_inicio, pendencia.data_fim, pendencia.status
            FROM '.\\data\\pendencia_ator.parquet' AS pendencia, '.\\data\\ator.parquet' AS ator
            WHERE pendencia.id_ator = ator.id_ator
            GROUP BY ALL
            ORDER BY 1;
            """
    conn.execute(sql)
    df: pd.DataFrame = conn.df()
    conn.close()
    return df

async def main():
    st.set_page_config(page_title="Pendências do Ator", page_icon="favicon.ico", layout="wide")
    #options = st.sidebar.multiselect('-----', descricoes, descricoes_escolhidas)
    st.text("Pendências do ator")
    df: pd.DataFrame = await get_dataframe()
    st.dataframe(df)
    btn = st.sidebar.button('Executar')
    if btn:
        pass

asyncio.run(main())