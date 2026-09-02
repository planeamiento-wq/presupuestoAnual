import streamlit as st
import pandas as pd

@st.cache_data
def cargar_datos_presupuesto():
    """
    Carga el archivo principal de presupuesto y normaliza las columnas de texto y numéricas.
    Usa caché para que la app no tenga que leer el disco en cada interacción.
    """
    # ruta del archivo con los datos
    path_archivo = "data/presupuesto.xlsx" 
    
    try:
        # leo el excel
        df = pd.read_excel(path_archivo)
        
        # 1. LIMPIEZA DE TEXTOS: Quitamos espacios rebeldes al inicio o final de las celdas
        columnas_texto = ['Sede', 'Tipo', 'Descripción tipo', 'Unidad', 'Sub unidad', 'Concepto']
        for col in columnas_texto:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
                
        # 2. LIMPIEZA DE NÚMEROS: Convertimos los meses a formato numérico puro.
        # Si encuentra celdas vacías o con guiones "-", las transforma en 0 automáticamente.
        meses = ['marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 
                 'septiembre', 'octubre', 'noviembre', 'diciembre', 'PRES. TOTAL']
        
        for mes in meses:
            if mes in df.columns:
                df[mes] = pd.to_numeric(df[mes], errors='coerce').fillna(0)
                
        return df
    
    except FileNotFoundError:
        st.error(f"No se encontró el archivo en la ruta: '{path_archivo}'. Asegúrate de crear la carpeta 'data' y guardar el Excel allí.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error inesperado al procesar el archivo Excel: {e}")
        return pd.DataFrame()


@st.cache_data
def cargar_datos_colaboradores():
    """
    Carga el Excel nominal de colaboradores/administrativos (un renglón por
    persona) y lo agrupa para producir el mismo formato que antes generaba
    actualizador.py contra la base de datos en vivo (colaboradores_area.parquet):
    columnas 'area', 'sede' y 'total'.

    Reemplaza la consulta a si_empleados: ya no se necesita conexión a la BD
    para este dato, se lee directamente del Excel que se actualiza a mano.
    """
    # ruta del archivo con el listado nominal de colaboradores
    path_archivo = "data/colaboradores.xlsx"

    columnas_esperadas = {
        "SEDE": "sede",
        "SERVICIOS/UNIDAD ACADÉMICA": "area",
    }

    try:
        df = pd.read_excel(path_archivo)

        faltantes = [c for c in columnas_esperadas if c not in df.columns]
        if faltantes:
            st.error(
                "Faltan columnas esperadas en el Excel de colaboradores: "
                f"{faltantes}"
            )
            return pd.DataFrame(columns=["area", "sede", "total"])

        df = df.rename(columns=columnas_esperadas)

        # Limpieza de textos: quitamos espacios rebeldes al inicio o final
        df["sede"] = df["sede"].astype(str).str.strip()
        df["area"] = df["area"].astype(str).str.strip()

        # Un renglón = un/a empleado/a -> contamos personas por área y sede
        df_agrupado = (
            df.groupby(["area", "sede"]).size().reset_index(name="total")
        )

        return df_agrupado

    except FileNotFoundError:
        st.error(
            f"No se encontró el archivo en la ruta: '{path_archivo}'. "
            "Asegúrate de guardar el Excel de colaboradores en la carpeta 'data'."
        )
        return pd.DataFrame(columns=["area", "sede", "total"])
    except Exception as e:
        st.error(f"Error inesperado al procesar el Excel de colaboradores: {e}")
        return pd.DataFrame(columns=["area", "sede", "total"])


@st.cache_data
def cargar_datos_administrativos():
    """
    Resumen de personas por servicio, a partir del mismo listado nominal
    (antes 'administrativos.parquet', generado desde la BD agrupando por la
    columna 'seccion'). El Excel actual solo trae una clasificación por
    área/servicio ('SERVICIOS/UNIDAD ACADÉMICA'), así que se reutiliza esa
    misma columna como 'servicio'.
    """
    df = cargar_datos_colaboradores()
    if df.empty:
        return pd.DataFrame(columns=["servicio", "total"])

    df_admin = (
        df.rename(columns={"area": "servicio"})
        .groupby("servicio")["total"]
        .sum()
        .reset_index()
    )
    return df_admin