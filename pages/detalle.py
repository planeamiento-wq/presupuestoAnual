import streamlit as st
from components.header import crear_header
from components.footer import crear_footer

# Importamos las vistas y la estructura de datos desde los módulos
from pages.detalleAcademico import cargar_vista_academica, PALETA_FACULTADES
from pages.detalleAdministrativo import cargar_vista_administrativa

def mostrar_detalle():
    crear_header(
        "DETALLE PRESUPUESTARIO",
        "Desglose pormenorizado de partidas académicas y administrativas"
    )
    
    # --------------------------------======
    # CONTENEDOR DE FILTROS EN PARALELO
    # --------------------------------======
    f_col1, f_col2 = st.columns([1, 2])
    
    with f_col1:
        tipo_detalle = st.radio(
            "Seleccione la categoría de análisis:", 
            ["Administrativo", "Académico"], 
            horizontal=True
        )
    with f_col2:
        if tipo_detalle == "Académico":
            opciones = list(PALETA_FACULTADES.keys())
            seleccion_filtro = st.selectbox("Seleccione Unidad Académica:", opciones)
        else:
            opciones = ["Todas las Áreas", "Gastos en Personal", "Gastos de Funcionamiento", "Inversiones Operativas"]
            seleccion_filtro = st.selectbox("Filtrar por Área / Dirección de Gasto:", opciones)
            
    st.markdown("---")
    
    # --------------------------------======
    # ORQUESTADOR DE REDIRECCIÓN MODULAR
    # --------------------------------======
    if tipo_detalle == "Académico":
        cargar_vista_academica(seleccion_filtro)
    else:
        cargar_vista_administrativa(seleccion_filtro)

    crear_footer()