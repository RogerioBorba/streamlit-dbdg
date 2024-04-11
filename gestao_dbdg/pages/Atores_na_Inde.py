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
            SELECT 
             nom_instituicao AS 'nome', 
             dsc_sigla AS 'sigla', 
             CASE 
                 WHEN ind_esfera = 1 THEN 'Estadual' 
                 WHEN ind_esfera = 2 THEN 'Federal'
                 WHEN ind_esfera = 3 THEN 'Municipal'
                 WHEN ind_esfera = 4 THEN 'Privada'
                 WHEN ind_esfera = 5 THEN 'Distrital'
                 else '-'
              END AS 'esfera',
              CASE 
                 WHEN ind_status = 1 THEN 'Interessado' 
                 WHEN ind_status = 2 THEN 'Aguardando Termo'
                 WHEN ind_status = 3 THEN 'Termo assinado'
                 WHEN ind_status = 4 THEN 'Configurado'
                 WHEN ind_status = 5 THEN 'Implantado'
                 WHEN ind_status = 6 THEN 'Desativado'
                 else '-'
              END AS 'status',
              CASE 
                 WHEN ind_modalidade = 1 THEN 'Central' 
                 WHEN ind_modalidade = 2 THEN 'Própria'
                 WHEN ind_modalidade = 3 THEN 'Mista'
                 else '-' 
              END AS 'modalidade',
              dat_interesse_adesao AS 'data_interesse_adesao',
              dat_adesao as 'data_adesao',
              dat_configuracao AS 'data_configuracao',
              dat_implantacao  AS 'data_implantacao'
             FROM '.\\data\\ator.parquet'
             GROUP BY ALL
             ORDER BY  1;
            """
    conn.execute(sql)
    df: pd.DataFrame = conn.df()
    conn.close()
    return df

async def main():
    df:pd.DataFrame = await get_dataframe()
    df_filtered: pd.DataFrame = df
    status = df['status'].unique()
    esferas = df['esfera'].unique()
    status_escolhidos = status
    selecionar_todas = st.sidebar.checkbox('Selecionar todos status')
    esferas_escolhidas = esferas
    if selecionar_todas:
        status_escolhidos = status

    options_status = st.sidebar.multiselect('-----', status, status_escolhidos)
    options_esfera = st.sidebar.multiselect('-----', esferas, esferas_escolhidas)
    if options_status:
        df_filtered = df.query(f"status in ({options_status}) and esfera in ({options_esfera})")
    st.write(f"Total de instituições em contato com o DBDG/INDE: {len(df_filtered)}")
    st.dataframe(df_filtered)


    c1, = st.columns(1)
    fig = px.bar(df_filtered, x= 'status', color='esfera')
    c1.plotly_chart(fig)
    btn = st.sidebar.button('Executar')
    if btn:
        print(f"status in ({status_escolhidos})")
asyncio.run(main())