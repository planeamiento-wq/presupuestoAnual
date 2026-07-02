import streamlit as st

def crear_kpi(titulo, valor, color_borde, variacion=None):
    # Armamos la base en una sola línea para evitar que Streamlit meta Markdown no deseado
    html = f'<div class="kpi-card {color_borde}"><div class="kpi-title">{titulo}</div><div class="kpi-value">{valor}</div>'

    # Si hay variación, la sumamos también en una sola línea limpia
    if variacion is not None:
        html += f'<div class="kpi-delta">{variacion} en la selección</div>'

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)