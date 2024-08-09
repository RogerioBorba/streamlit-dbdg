import asyncio

import streamlit as st


async def main():
    st.title("Gestão de serviços do DBDG")
    st.text("Consultas sobre diferentes aspectos dos serviços WMS, WFS, CSW no DBDG da INDE")
    

if __name__ == "__main__":
    asyncio.run(main())