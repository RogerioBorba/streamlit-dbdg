#import streamlit as st
from streamlit_folium import st_folium
import folium
m = folium.Map(location=[-25,-57], zoom_start=4)
st_data = st_folium(m, width= '100vw')