import asyncio
import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

async def get_dataframe_atores_capacitados() -> pd.DataFrame:
    conn = duckdb.connect()
    conn.install_extension("parquet")
    conn.load_extension("parquet")
    sql: str = """
            SELECT "nome_instituicao" as 'instituicao', COUNT("nome_instituicao") as 'qtd_turma', sum("numero_de_participantes")::INTEGER as 'qtd_participante' 
            FROM '.\\data\\atores_capacitados.parquet'
            GROUP BY ALL
            ORDER BY 1;
            """
    conn.execute(sql)
    df_capacitados: pd.DataFrame = conn.df()
    conn.close()
    return df_capacitados

async def get_dataframe_atores_capacitados_por_ano() -> pd.DataFrame:
    conn = duckdb.connect()
    conn.install_extension("parquet")
    conn.load_extension("parquet")
    sql: str = """
            SELECT ano, sum(numero_de_participantes) as 'numero_de_participantes'  
            FROM '.\\data\\atores_capacitados.parquet'
            GROUP BY ano, 
            ORDER BY 1;
            """
    conn.execute(sql)
    df: pd.DataFrame = conn.df()
    conn.close()
    return df

async def main():
    st.set_page_config(page_title="Atores capacitados", page_icon="favicon.ico", layout="wide")
    #options = st.sidebar.multiselect('-----', descricoes, descricoes_escolhidas)
    df: pd.DataFrame = await get_dataframe_atores_capacitados()
    st.write(f"Atores capacitados.Quantidade total de participantes: {sum(df['qtd_participante'])}")
    st.dataframe(df, use_container_width=True)
    st.write(" ")
    st.write("Atores capacitados por ano")
    df1: pd.DataFrame = await get_dataframe_atores_capacitados_por_ano()
    #st.dataframe(df1, column_config={"ano": st.column_config.NumberColumn(format="%d")})
    #print(df1['ano'].dtype)
    fig1 = px.bar(df1, x='ano', y='numero_de_participantes')
    st.plotly_chart(fig1)
    btn = st.sidebar.button('Executar')
    if btn:
        pass
asyncio.run(main())