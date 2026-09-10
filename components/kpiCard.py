import streamlit as st

def crear_kpi_html(titulo, valor, color_borde, variacion=None):
    """Devuelve el HTML de la tarjeta KPI (sin renderizar), para poder
    combinar varias en un solo contenedor grid responsive."""
    # Armamos la base en una sola línea para evitar que Streamlit meta Markdown no deseado
    html = f'<div class="kpi-card {color_borde}"><div class="kpi-title">{titulo}</div><div class="kpi-value">{valor}</div>'

    # Si hay variación, la sumamos también en una sola línea limpia
    if variacion is not None:
        html += f'<div class="kpi-delta">{variacion} en la selección</div>'

    html += "</div>"
    return html


def crear_kpi(titulo, valor, color_borde, variacion=None):
    """Mantiene el comportamiento original: renderiza una sola tarjeta.
    Se conserva para no romper otros usos existentes."""
    st.markdown(
        crear_kpi_html(titulo, valor, color_borde, variacion),
        unsafe_allow_html=True,
    )