import asyncio
import streamlit as st
import duckdb
import pandas as pd
import base64
import io


class HitoricoAtor:

    def __init__(self):
        self.conn = duckdb.connect()


    #def __del__(self):
     #   print('Destructor called, Objeto HistoricoAtor deleted.')
     #self.conn.close()

    async def get_pdf_from_hitorico(self, id_historico: int):
        sql: str = f"""
                       SELECT arq_historico
                       FROM '.\\data\\historico_ator.parquet' AS historico
                       WHERE id_historico_ator = {id_historico}
                       """

        results = duckdb.sql(sql).fetchone()
        #pdf_bytes = base64.b64decode(results[0])

        return results[0]

    async def get_dataframe(self) -> pd.DataFrame:
        sql: str = """
                SELECT * EXCLUDE (arq_historico)
                FROM '.\\data\\historico_ator.parquet' AS historico
                """
        self.conn.execute(sql)
        df: pd.DataFrame = self.conn.df()
        return df


async def main():
    st.set_page_config(page_title="Histórico do Ator", page_icon="favicon.ico", layout="wide")
    historico_ator = HitoricoAtor()
    df: pd.DataFrame = await historico_ator.get_dataframe()
    st.text(f"Histórico do ator: {len(df)}")
    selected = st.dataframe(data=df,  use_container_width=True, hide_index=True, selection_mode="single-row", on_select="rerun")
    rows = selected.selection['rows']
    if rows:
        id_historico = df.iloc[rows[0]]['id_historico_ator']
        pdf_bytes = await historico_ator.get_pdf_from_hitorico(id_historico)
        #st.download_button(label="📄 Baixar PDF", data=pdf_bytes, file_name=f"historico_ator.pdf",mime="application/pdf")
        st.write("Pré-visualização do PDF:")
        pdf_base64_string = base64.b64encode(pdf_bytes).decode('utf-8')  # Re-encode para string Base64
        pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_base64_string}" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

asyncio.run(main())