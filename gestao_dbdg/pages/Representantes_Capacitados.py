import asyncio
import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px



def init_duckdb_connnection() -> duckdb.DuckDBPyConnection:
    conn = duckdb.connect()
    conn.install_extension("parquet")
    conn.load_extension("parquet")
    return conn


async def get_dataframe(conn: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    sql: str = """
            SELECT *
            FROM '.\\data\\representantes_ator.parquet'
            GROUP BY ALL
            ORDER BY 1;
            """
    conn.execute(sql)
    df: pd.DataFrame = conn.df()
    return df

async def get_dataframe_group_by(conn: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    sql: str = """
            SELECT nome_ator, count(nome_ator) as qtd_representante
            FROM '.\\data\\representantes_ator.parquet'
            GROUP BY ALL
            ORDER BY 1;
            """
    conn.execute(sql)
    df: pd.DataFrame = conn.df()
    return df


async def get_dataframe_atores_representantes_capacitados_turma(conn: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    sql: str = """
            SELECT a.dsc_sigla, r.nom_representante, strftime(t.dat_inicio, '%Y-%m-%d') AS Data, t.nom_turma, t.dsc_turma
            FROM '.\\data\\turma.parquet' AS t,
                 '.\\data\\participante_turma.parquet' AS pt,
                '.\\data\\representante.parquet' AS r,
                '.\\data\\ator.parquet' AS a   
            WHERE t.id_turma = pt.id_turma 
            AND pt.id_representante = r.id_representante
            AND r.id_ator = a.id_ator
            ORDER BY 1;
            """
    conn.execute(sql)
    df: pd.DataFrame = conn.df()
    return df


async def get_dataframe_turmas_por_ano(conn: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    sql: str = """
            SELECT YEAR(dat_inicio) as 'ano', count(*) as 'qtd_turma' 
            FROM '.\\data\\turma.parquet'
            GROUP BY YEAR(dat_inicio), 
            ORDER BY 1;
            """
    conn.execute(sql)
    df: pd.DataFrame = conn.df()
    return df


async def main():
    conn: duckdb.DuckDBPyConnection = init_duckdb_connnection()
    st.set_page_config(page_title="Representantes capacitados", page_icon="favicon.ico", layout="wide")
    #options = st.sidebar.multiselect('-----', descricoes, descricoes_escolhidas)
    st.text("Instituições e quantidade de representantes capacitados")
    st.dataframe(await get_dataframe_group_by(conn), use_container_width=True)

    st.text("")
    st.text("Atores e seus representantes capacitados por turma")
    df: pd.DataFrame = await get_dataframe_atores_representantes_capacitados_turma(conn)
    st.dataframe(df)
    st.text("")
    st.text("Capacitações realizadas ao longo dos anos")
    df2: pd.DataFrame = await get_dataframe_turmas_por_ano(conn)
    fig2 = px.bar(df2, x='ano', y='qtd_turma')
    st.plotly_chart(fig2)

    btn = st.sidebar.button('Executar')
    if btn:
        pass
    conn.close()

asyncio.run(main())