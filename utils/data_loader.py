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
        st.error(f"⚠️ No se encontró el archivo en la ruta: '{path_archivo}'. Asegúrate de crear la carpeta 'data' y guardar el Excel allí.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error inesperado al procesar el archivo Excel: {e}")
        return pd.DataFrame()