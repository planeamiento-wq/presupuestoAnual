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
    # CONTENEDOR DE FILTROS EN PARALELO (4 Columnas)
    # --------------------------------======
    # Ajustamos las proporciones para que el radio y el selectbox principal tengan buen espacio
    f_col1, f_col2, f_col3, f_col4 = st.columns([1.5, 2, 1.2, 1.2])
    
    with f_col1:
        tipo_detalle = st.radio(
            "Categoría de análisis:", 
            ["Administrativo", "Académico"], 
            horizontal=True
        )
        
    with f_col2:
        if tipo_detalle == "Académico":
            opciones = list(PALETA_FACULTADES.keys())
            seleccion_filtro = st.selectbox("Seleccione Unidad Académica:", opciones)
        else:
            opciones = ["Todas las Áreas", "Adm. General", "Alumnos", "Tesorería"]
            seleccion_filtro = st.selectbox("Filtrar por Área / Dirección de Gasto:", opciones)
            
    with f_col3:
        # Filtro independiente de Sede
        seleccion_sede = st.selectbox(
            "Sede:",
            ["Todas las Sedes", "CENTRAL", "CONCEPCIÓN", "BUENOS AIRES"],
            key="filtro_sede_global"
        )
        
    with f_col4:
        # Filtro independiente de Mes
        seleccion_mes = st.selectbox(
            "Mes:",
            [
                "Anual (Ene-Dic)", "Enero", "Febrero", "Marzo", "Abril", "Mayo", 
                "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
            ],
            key="filtro_mes_global"
        )
            
    st.markdown("---")
    
    # --------------------------------======
    # ORQUESTADOR DE REDIRECCIÓN MODULAR
    # --------------------------------======
    # Pasamos de forma transparente la selección del filtro principal, la sede y el mes
    if tipo_detalle == "Académico":
        cargar_vista_academica(seleccion_filtro, sede=seleccion_sede, mes=seleccion_mes)
    else:
        cargar_vista_administrativa(seleccion_filtro, sede=seleccion_sede, mes=seleccion_mes)

    crear_footer()