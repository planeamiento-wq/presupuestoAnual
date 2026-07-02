import streamlit as st
import pandas as pd
from components.header import crear_header
from components.footer import crear_footer

def mostrar_detalle():
    # Ponemos la cabecera usando tu componente institucional
    crear_header(
        "DETALLE PRESUPUESTARIO",
        "Desglose pormenorizado de partidas académicas y administrativas"
    )
    
    # 1. Filtro principal en botones horizontales
    tipo_detalle = st.radio(
        "Seleccione la categoría de análisis:", 
        ["Administrativo", "Académico"], 
        horizontal=True
    )
    
    st.markdown("---")
    
    # ==========================================
    # SECCIÓN A: ADMINISTRATIVO
    # ==========================================
    if tipo_detalle == "Administrativo":
        st.markdown("### Gasto Operativo y de Funcionamiento")
        
        # Opciones para el segundo filtro de administración
        areas_admin = ["Todas las Áreas", "Gastos en Personal", "Gastos de Funcionamiento", "Inversiones Operativas"]
        area_seleccionada = st.selectbox("Filtrar por Área / Dirección de Gasto:", areas_admin)
        
        # Datos extraídos de tu PDF de la UNSTA
        datos_admin = {
            "Área / Dirección de Gasto": ["Gastos en Personal", "Gastos de Funcionamiento", "Inversiones Operativas"],
            "Presupuesto Proyectado 2026": [18770841602.36, 4503854678.30, 1231782442.70]
        }
        df_admin = pd.DataFrame(datos_admin)
        
        # Si eligen un área específica, filtramos el cuadro
        if area_seleccionada != "Todas las Áreas":
            df_admin = df_admin[df_admin["Área / Dirección de Gasto"] == area_seleccionada]
            
        # Formateamos el número para que aparezca lindo como moneda ($ 1.234,56)
        df_admin["Monto Proyectado"] = df_admin["Presupuesto Proyectado 2026"].map(
            lambda x: f"$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )
        
        # Mostramos la tabla limpia en pantalla
        st.dataframe(
            df_admin[["Área / Dirección de Gasto", "Monto Proyectado"]], 
            use_container_width=True, 
            hide_index=True
        )
        
    # ==========================================
    # SECCIÓN B: ACADÉMICO (Con colores pasteles requeridos)
    # ==========================================
    else:
        st.markdown("### Presupuesto por Unidad Académica")
        
        # Diccionario con los colores pasteles oficiales de cada facultad
        COLORES_UNIDADES = {
            "Facultad de Economía y Administración": "background-color: #B8E3C6; color: #10381e; font-weight: bold;",
            "Facultad de Ciencias Jurídicas": "background-color: #F3C4D6; color: #4a1228; font-weight: bold;",
            "Facultad de Ingeniería": "background-color: #AEC6CF; color: #0f2730; font-weight: bold;",
            "Facultad de Humanidades": "background-color: #F9E7A3; color: #42380a; font-weight: bold;",
            "Facultad de Ciencias de la Salud": "background-color: #E8D7F1; color: #2e103d; font-weight: bold;"
        }
        
        # Creamos las opciones del buscador sumando la opción de ver todas
        unidades_filtro = ["Todas las Facultades"] + list(COLORES_UNIDADES.keys())
        unidad_seleccionada = st.selectbox("Filtrar por Unidad Académica:", unidades_filtro)
        
        # Datos simulados del borrador
        datos_acad = {
            "Unidad Académica": list(COLORES_UNIDADES.keys()),
            "Alumnos Activos Est.": [2100, 1450, 890, 620, 1780],
            "Participación %": ["25%", "18%", "12%", "10%", "22%"],
            "Asignación Presupuestaria": ["$ 7.160.000.000", "$ 5.155.000.000", "$ 3.437.000.000", "$ 2.864.000.000", "$ 6.290.000.000"]
        }
        df_acad = pd.DataFrame(datos_acad)
        
        # Filtramos la tabla si eligen una facultad sola
        if unidad_seleccionada != "Todas las Facultades":
            df_acad = df_acad[df_acad["Unidad Académica"] == unidad_seleccionada]
        
        # Función mágica de Pandas para pintar la celda según la facultad
        def colorear_columna(val):
            return COLORES_UNIDADES.get(val, '')
            
        # Le aplicamos el color pastel solo a la columna "Unidad Académica"
        df_estilado = df_acad.style.map(colorear_columna, subset=["Unidad Académica"])
        
        # Mostramos la tabla en pantalla
        st.dataframe(df_estilado, use_container_width=True, hide_index=True)

    # Cerramos con tu pie de página institucional
    crear_footer()