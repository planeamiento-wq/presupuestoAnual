import streamlit as st
import pandas as pd
from utils.conexion import ejecutar_sql

@st.cache_data(ttl=300)
def obtener_resumen_ingresantes_historico():
    query = """
        SELECT
            Sede as sede,
            Cohorte as anio,
            TRIM(Facultad) as unidad,
            SUM(Inscriptos) AS total
        FROM si_inscriptos_7_anios
        where Cohorte >= (year(now()) - 2) and Facultad != "FILOSOFÍA"
        group by Sede, Cohorte, TRIM(Facultad), Carrera;
    """
    try:
        df = ejecutar_sql(query)
        if df is not None and not df.empty:
            return df
        return pd.DataFrame(columns=["sede", "unidad", "anio", "total"])
    except Exception as e:
        st.error(f"Error al consultar si_inscriptos_7_anios: {e}")
        return pd.DataFrame(columns=["sede", "unidad", "anio", "total"])