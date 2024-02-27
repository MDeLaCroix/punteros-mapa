# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import folium
import base64

LOGGER = get_logger(__name__)

def make_map(file):
    df = pd.read_excel(file)
    final_map = folium.Map(location=[23.634501, -102.552784], zoom_start=5)

    for _, tienda in df.iterrows():
        folium.Marker(location=[tienda['Latitud'], tienda['Longitud']],
                      popup=tienda['Nombre'],
                      icon=folium.Icon(color=tienda['Color'],
                                       prefix='fa',
                                       icon='fa-shopping-cart')).add_to(final_map)
    return final_map

def download_link(mapa):
    mapa.save('mapa_temporal.html')
    with open('mapa_temporal.html', 'r', encoding='utf-8') as f:
        html_string = f.read()

    # Codificar el HTML en base64
    b64 = base64.b64encode(html_string.encode()).decode()

    # Crear el enlace de descarga
    href = f'<a href="data:text/html;base64,{b64}" download="mapa_interactivo.html">Descargar mapa interactivo</a>'
    return href

def run():
    st.set_page_config(
        page_title="Main",
        page_icon="👋",
    )

    st.title("Generador de Mapa con Folium")

    st.markdown(
        """
        Sube un archivo Excel con las columnas:
        - Nombre,
        - Latitud,
        - Longitud,
        - Color,
        - Símbolo.
        """
    )

    excel_file = st.file_uploader("Elige un archivo Excel", type=['xlsx'])

    if excel_file is not None:
    # Generar el mapa
        mapa = make_map(excel_file)
        mapa_enlace = download_link(mapa)

    # Permitir la descarga del mapa como HTML
        st.markdown(mapa_enlace, unsafe_allow_html=True)

if __name__ == "__main__":
    run()
