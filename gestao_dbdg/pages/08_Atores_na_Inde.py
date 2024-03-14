import asyncio
import streamlit as st
import duckdb
import pandas as pd

async def main():
    st.set_page_config(page_title="Atores", page_icon="favicon.ico", layout="wide")
    #options = st.sidebar.multiselect('-----', descricoes, descricoes_escolhidas)
    conn = duckdb.connect()
    conn.install_extension("parquet")
    conn.load_extension("parquet")
    sql: str = """
        SELECT *
        FROM '.\\data\\atores_na_inde_por_modalidade.parquet'
        GROUP BY ALL
        ORDER BY 1;
        """
    conn.execute(sql)
    df_capacitados: pd.DataFrame = conn.df()
    st.dataframe(df_capacitados)
    c1, c2 = st.columns(2)
    c1.write(f"Quantidade total de turmas: {sum(df_capacitados['qtd_turma'])}")
    c2.write(f"Quantidade total de participantes: {sum(df_capacitados['qtd_participante'])}")
    conn.close()
    btn = st.sidebar.button('Executar')
    if btn:
        pass

asyncio.run(main())