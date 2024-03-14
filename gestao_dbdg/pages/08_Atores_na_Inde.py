import asyncio
import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px


async def get_dataframe() -> pd.DataFrame:
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
    df: pd.DataFrame = conn.df()
    conn.close()
    return df

async def main():
    df:pd.DataFrame = await get_dataframe()
    df_filtered: pd.DataFrame = df
    status = df['status'].unique()
    status_escolhidos = status
    selecionar_todas = st.sidebar.checkbox('Selecionar todos status')

    if selecionar_todas:
        status_escolhidos = status

    options = st.sidebar.multiselect('-----', status, status_escolhidos)
    if options:
        df_filtered = df.query(f"status in ({options})")
    st.dataframe(df_filtered)
    st.write(f"Total selecionado: {len(df_filtered)}")


    c1, = st.columns(1)
    fig = px.bar(df, x= 'status', color='esfera')
    c1.plotly_chart(fig)
    btn = st.sidebar.button('Executar')
    if btn:
        print(f"status in ({status_escolhidos})")
asyncio.run(main())