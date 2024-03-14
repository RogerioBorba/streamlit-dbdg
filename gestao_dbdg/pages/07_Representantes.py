import asyncio
import streamlit as st
import duckdb
import pandas as pd


async def get_dataframe() -> pd.DataFrame:
    conn = duckdb.connect()
    sql: str = """
            SELECT *
            FROM '.\\data\\representantes_ator.parquet'
            GROUP BY ALL
            ORDER BY 1;
            """
    conn.execute(sql)
    df: pd.DataFrame = conn.df()
    conn.close()
    return df

async def get_dataframe_group_by() -> pd.DataFrame:
    conn = duckdb.connect()
    sql: str = """
            SELECT nome_ator, count(nome_ator) as qtd_representante
            FROM '.\\data\\representantes_ator.parquet'
            GROUP BY ALL
            ORDER BY 1;
            """
    conn.execute(sql)
    df: pd.DataFrame = conn.df()
    conn.close()
    return df

async def get_dataframe_gestor() -> pd.DataFrame:
    conn = duckdb.connect()
    sql: str = """
            SELECT nome_ator, nome_representante, email
            FROM '.\\data\\representantes_ator.parquet'
            where e_gestor = 'Sim'
            ORDER BY 1;
            """
    conn.execute(sql)
    df: pd.DataFrame = conn.df()
    conn.close()
    return df

async def main():
    st.set_page_config(page_title="Atores capacitados", page_icon="favicon.ico", layout="wide")
    #options = st.sidebar.multiselect('-----', descricoes, descricoes_escolhidas)
    st.text("Instituições e quantidade de representantes capacitados")
    st.dataframe(await get_dataframe_group_by())
    st.text("Gestores")
    st.dataframe(await get_dataframe_gestor())
    df: pd.DataFrame = await get_dataframe()
    st.dataframe(df)
    btn = st.sidebar.button('Executar')
    if btn:
        pass

asyncio.run(main())