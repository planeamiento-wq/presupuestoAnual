from datetime import datetime

import streamlit as st
import pandas as pd

RUTA_PARQUET = "data/inscriptos_7_anios.parquet"

@st.cache_data(ttl=300)
def obtener_resumen_ingresantes_historico():
    """Replica localmente la consulta que antes se ejecutaba en vivo contra
    si_inscriptos_7_anios, a partir del parquet que genera actualizador.py."""
    try:
        df = pd.read_parquet(RUTA_PARQUET)
        if df is None or df.empty:
            return pd.DataFrame(columns=["sede", "unidad", "anio", "total"])

        anio_corte = datetime.now().year - 2
        df = df[
            (df["Cohorte"] >= anio_corte) & (df["Facultad"] != "FILOSOFÍA")
        ].copy()
        df["Facultad"] = df["Facultad"].astype(str).str.strip()

        resumen = (
            df.groupby(["Sede", "Cohorte", "Facultad"], as_index=False)["Inscriptos"]
            .sum()
            .rename(
                columns={
                    "Sede": "sede",
                    "Cohorte": "anio",
                    "Facultad": "unidad",
                    "Inscriptos": "total",
                }
            )
        )
        return resumen
    except FileNotFoundError:
        st.error(
            f"⚠️ No se encontró '{RUTA_PARQUET}'. Ejecutá actualizador/actualizador.py"
            " para generar los datos."
        )
        return pd.DataFrame(columns=["sede", "unidad", "anio", "total"])
    except Exception as e:
        st.error(f"Error al procesar si_inscriptos_7_anios: {e}")
        return pd.DataFrame(columns=["sede", "unidad", "anio", "total"])