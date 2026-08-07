import streamlit as st
import pandas as pd
from utils.conexion import ejecutar_sql

@st.cache_data(ttl=300)
def obtener_resumen_ingresantes_historico():
    query = """
        SELECT 
            periodo AS anio, 
            sede,
            COALESCE(NULLIF(TRIM(unidad), ''), 'Diplomatura UNSTA') AS unidad,
            COUNT(id_alumno) AS total
        FROM si_inscriptos_2025
        GROUP BY sede, COALESCE(NULLIF(TRIM(unidad), ''), 'Diplomatura UNSTA'), periodo
        
        UNION ALL
        
        SELECT 
            periodo AS anio, 
            sede,
            COALESCE(NULLIF(TRIM(unidad), ''), 'Diplomatura UNSTA') AS unidad,
            COUNT(id_alumno) AS total
        FROM si_inscriptos_2026
        GROUP BY sede, COALESCE(NULLIF(TRIM(unidad), ''), 'Diplomatura UNSTA'), periodo;
    """
    try:
        df = ejecutar_sql(query)
        if df is not None and not df.empty:
            return df
        return pd.DataFrame(columns=['anio', 'sede', 'unidad', 'total'])
    except Exception as e:
        st.error(f"Error al consultar las vistas de 2025 y 2026: {e}")
        return pd.DataFrame(columns=['anio', 'sede', 'unidad', 'total'])