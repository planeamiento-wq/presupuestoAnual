import streamlit as st
import pandas as pd
from styles.styles import cargar_estilo
from components.header import crear_header
from components.footer import crear_footer
from components.kpiCard import crear_kpi
from components.card import abrir_card, cerrar_card
from pages.Resumen import mostrar_resumen
from pages.detalle import mostrar_detalle
from pages.ingresoHistorico import mostrar_historico

try:
    from Resumen import mostrar_resumen
except ImportError:
    # Por si acaso  dentro de  carpeta pages/
    from pages.Resumen import mostrar_resumen

# CONFIGURACIÓN DE PÁGINA GLOBALES
st.set_page_config(
    page_title = "Presupuesto Institucional",
    layout="wide"
)

# Llamo al CSS global
cargar_estilo()

# ==== MENÚ LATERAL (Sidebar) ====
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#005088; margin-top:20px;'>Menú Presupuesto</h2>", unsafe_allow_html=True)
    
    # Selector de páginas
    opcion_menu = st.radio(
        "Navegación:",
        ["Inicio", "Resumen Ejecutivo", "Detalle Presupuestario", "Gráficos Históricos"],
        label_visibility="collapsed"
    )
    
    #st.markdown("### Filtros Globales")
    #sede = st.selectbox("Sede:", ["Sede Central", "Sede Concepción", "Sede Yerba Buena"])
    #Smes_corte = st.select_slider("Mes de corte:", options=["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"], value="Jun")


# ==== LÓGICA DE NAVEGACIÓN ====

# Caso A: Si el usuario elige "Inicio / Portada", ejecutamos tu código original de portada
if opcion_menu == "Inicio":
    # BANNER
    col1, col2, col3 = st.columns([1,8,1])
    with col2:
        st.image(
            "assets/banner3.png",
            width="stretch"
        )

    # TÍTULOS
    st.markdown(
        """
        <div class='titulo-portada'>
            PRESUPUESTO INSTITUCIONAL
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='subtitulo-portada'> 2026 </div>
        """,
        unsafe_allow_html=True
    )

    # DESCRIPCIÓN
    st.markdown(
        """
        <div class='descripcion'>
            Proyección y seguimiento de ingresos, egresos, inversiones y resultados institucionales.
        </div>
        """,
        unsafe_allow_html=True
    )
    
    crear_footer()

# Caso B: Si elige "Resumen Ejecutivo", abrimos la "caja" de tu componente
elif opcion_menu == "Resumen Ejecutivo":
    mostrar_resumen()

# Caso C: Espacio reservado para lo que hagamos después
elif opcion_menu == "Detalle Presupuestario":
    mostrar_detalle()

# Caso D: Espacio reservado para los gráficos interanuales
elif opcion_menu == "Gráficos Históricos":
    mostrar_historico()