import asyncio
import streamlit as st
import duckdb
import pandas as pd

async def main():
    st.set_page_config(page_title="Atores capacitados", page_icon="favicon.ico", layout="wide")
    #options = st.sidebar.multiselect('-----', descricoes, descricoes_escolhidas)
    conn = duckdb.connect()
    sql: str = """
        SELECT *
        FROM '.\\data\\representantes_ator.parquet'
        GROUP BY ALL
        ORDER BY 1;
        """
    conn.execute(sql)
    df: pd.DataFrame = conn.df()
    st.table(df)
    c1, c2 = st.columns(2)
    conn.close()
    btn = st.sidebar.button('Executar')
    if btn:
        pass

asyncio.run(main())