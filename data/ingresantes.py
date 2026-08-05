import streamlit as st
import pandas as pd
from utils.conexion import ejecutar_sql

@st.cache_data(ttl=300)
def obtener_resumen_ingresantes_historico():

    query = """
        SELECT 2025 AS anio, sede, COUNT(*) AS total
        FROM si_inscriptos_2025
        GROUP BY sede
        
        UNION ALL
        
        SELECT 2026 AS anio, sede, COUNT(*) AS total
        FROM si_inscriptos_2026
        GROUP BY sede;
    """
    try:
        return ejecutar_sql(query)
    except Exception as e:
        st.error(f"Error al consultar las vistas de 2025 y 2026: {e}")
        return pd.DataFrame()