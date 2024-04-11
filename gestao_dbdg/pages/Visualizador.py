import asyncio
import streamlit as st
from streamlit_folium import st_folium
import folium
from gestao_dbdg.src.capabilities.wms_get_capabilities import WMSCapabilities
from gestao_dbdg.src.inde_dbdg.inde import wms_capabilities_catalogo_inde
from collections import namedtuple
from gestao_dbdg.src.wms.wms_layer import WMSLayer

fmap = None

async def add_wms_layer(layer: WMSLayer):
    global fmap
    print(f"layer.url: {layer.url}")
    folium.LayerControl().add_to(fmap)
    folium.WmsTileLayer(
        url="https://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi",
        name="test",
        fmt="image/png",
        layers="nexrad-n0r-900913",
        attr=u"Weather data © 2012 IEM Nexrad",
        transparent=True,
        overlay=True,
        control=True,
    ).add_to(fmap)

async def display_wms_tree(desc_sigla_url: namedtuple):
    wms_capa = WMSCapabilities(desc_sigla_url.url, desc_sigla_url.sigla, desc_sigla_url.url)
    try:
        await wms_capa.execute_request()
        #return print(type(wms_capa.wms_layers()[0]))
        layers = (layer for layer in wms_capa.wms_layers() if layer.type() == 'Layer')
        for idx, layer in enumerate(layers):
            container = st.container()
            with container:
                c1,c2 = st.columns([3,1])
                with c1:
                    st.text(layer.title())
                with c2:
                    if st.button(":heavy_plus_sign:",key=f"{layer.title()}_{idx}"):  #on_click=add_wms_layer, args=[layer]
                        await add_wms_layer(layer)

                link = next(( i for i in layer.url_metadado_links()), None)
                if link:
                    st.link_button("metadado", link)
                else:
                    st.text("sem metadados")
    except Exception as e:
        print(e)
        st.text("Requisição falhou.")
async def wms_por_instituicao():
    l_descricao_sigla_url: list[namedtuple] = await wms_capabilities_catalogo_inde()
    wms_descricoes = [ desc_sigla_url.descricao for desc_sigla_url in l_descricao_sigla_url ]
    option = st.selectbox('Escolha a instituição desejada', wms_descricoes, index=None,
   placeholder="Escolha uma instituição",)
    if option:
        desc_sigla_url = next((item for item in l_descricao_sigla_url if item.descricao == option), None)
        await display_wms_tree(desc_sigla_url)


async def init_map():
    global fmap
    fmap = folium.Map(location=[-25,-57], zoom_start=4)
    # Adicionar o mapa ao Streamlit
    st_data = st_folium(fmap, width=725)
    return st_data

async def init_sidebar():
    with st.sidebar:
        st.header("Visualizador")
        with st.expander("WMS - buscar geosserviços da INDE"):
            tab1, tab2, tab3 = st.tabs(["Por instituição", "Por Nome/Título", "Por palavra chave"])
            with tab1:
                await wms_por_instituicao()
            with tab2:
                st.header("Por Nome/Título")
            with tab3:
                st.header("Por palavra chave")

async def main():
    tasks = []
    task = asyncio.create_task(init_map())
    tasks.append(task)
    task = asyncio.create_task(init_sidebar())
    tasks.append(task)
    await asyncio.gather(*tasks)

asyncio.run(main())