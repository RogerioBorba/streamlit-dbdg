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


async def get_dataframe_atores_capacitados(conn: duckdb.DuckDBPyConnection) -> pd.DataFrame:

    sql: str = """
            SELECT  capacitados.nome_instituicao as 'instituicao', COUNT(capacitados.nome_instituicao) as 'qtd_turma', sum(capacitados.numero_de_participantes)::INTEGER as 'qtd_participante', atores.esfera
            FROM 'C:\\dados\\IBGE\\gestao\\atores_na_inde_por_modalidade.parquet' as atores,
                 'C:\\dados\\IBGE\\gestao\\atores_capacitados.parquet' as capacitados  
            WHERE atores.nome_ator = capacitados.nome_instituicao
            GROUP BY ALL 
            ORDER BY 1;
            """
    conn.execute(sql)
    df_capacitados: pd.DataFrame = conn.df()
    return df_capacitados


async def get_dataframe_atores_representantes_capacitados(conn: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    sql: str = """
    SELECT instituicao, 
            count(turma)::INTEGER AS 'qtd_turma', 
            sum(qtd_treinado)::INTEGERgit AS 'qtd_treinado', 
            esfera 
            FROM (SELECT ator.nom_instituicao AS 'instituicao',turma.nom_turma AS 'turma',  COUNT(turma.nom_turma) AS 'qtd_treinado', 
            CASE 
                 WHEN ator.ind_esfera = 1 THEN 'Estadual' 
                 WHEN ator.ind_esfera = 2 THEN 'Federal'
                 WHEN ator.ind_esfera = 3 THEN 'Municipal'
                 WHEN ator.ind_esfera = 4 THEN 'Privada'
                 WHEN ator.ind_esfera = 5 THEN 'Distrital'
                 else '-'
              END AS 'esfera'  
                        FROM '.\\data\\turma.parquet' AS 'turma',
                             '.\\data\\participante_turma.parquet' AS 'part_turma',
                             '.\\data\\representante.parquet' AS 'repr',
                             '.\\data\\ator.parquet' AS 'ator'
                        WHERE turma.id_turma =  part_turma.id_turma AND 
                              part_turma.id_representante = repr.id_representante AND
                              repr.id_ator = ator.id_ator
                        GROUP BY ALL
                        ORDER BY 1)
                 GROUP BY ALL
                 ORDER BY 1;
            """
    conn.execute(sql)
    df: pd.DataFrame = conn.df()
    return df

async def get_dataframe_atores_capacitados_por_ano(conn: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    sql: str = """
            SELECT ano, sum(numero_de_participantes) as 'numero_de_participantes'  
            FROM '.\\data\\atores_capacitados.parquet'
            GROUP BY ano, 
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
    st.set_page_config(page_title="Atores capacitados", page_icon="favicon.ico", layout="wide")
    #options = st.sidebar.multiselect('-----', descricoes, descricoes_escolhidas)
    conn = init_duckdb_connnection()
    df_ator_rep = await get_dataframe_atores_representantes_capacitados(conn)
    st.write(
        f"Atores capacitados: {len(df_ator_rep['instituicao'].unique())}. Quantidade total de participantes: {sum(df_ator_rep['qtd_treinado'])}")
    st.dataframe(df_ator_rep, use_container_width=True)
    df: pd.DataFrame = await get_dataframe_atores_capacitados(conn)
    esferas = df['esfera'].unique()
    esferas_escolhidas = esferas
    options_esfera = st.sidebar.multiselect('-----', esferas, esferas_escolhidas)
    df_filtered = df.query(f"esfera in ({options_esfera})")
    st.write(
        f"Atores capacitados: {len(df_filtered['instituicao'].unique())}. Quantidade total de participantes: {sum(df_filtered['qtd_participante'])}")
    st.dataframe(df_filtered, use_container_width=True)
    st.write(" ")
    st.write("Atores capacitados por ano")
    df1: pd.DataFrame = await get_dataframe_atores_capacitados_por_ano(conn)
    #st.dataframe(df1, column_config={"ano": st.column_config.NumberColumn(format="%d")})
    #print(df1['ano'].dtype)
    fig1 = px.bar(df1, x='ano', y='numero_de_participantes')

    st.plotly_chart(fig1)
    st.write("Turmas por ano")
    df2: pd.DataFrame = await get_dataframe_turmas_por_ano(conn)
    fig2 = px.bar(df2, x='ano', y='qtd_turma')

    st.plotly_chart(fig2)
    btn = st.sidebar.button('Executar')
    conn.close()
    if btn:
        pass
asyncio.run(main())