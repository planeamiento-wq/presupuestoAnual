import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

@st.cache_resource
def obtener_engine():
    """Crea y mantiene viva la conexión a MySQL usando las credenciales de secrets.toml"""
    db = st.secrets["mysql"]
    port = db.get("port", 3306)
    url = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}:{port}/{db['database']}"
    return create_engine(url, pool_pre_ping=True)

def ejecutar_sql(query: str, params: dict = None) -> pd.DataFrame:
    """Función auxiliar para ejecutar cualquier SQL y devolver un DataFrame"""
    engine = obtener_engine()
    with engine.connect() as conn:
        return pd.read_sql(query, conn, params=params)

'''import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

@st.cache_resource
def obtener_engine():
    #crea y mantiene activa la conexión a MySQL
    db = st.secrets["mysql"]
    # Usamos pymysql como driver con SQLAlchemy
    url = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}:{db['port'] if 'port' in db else 3306}/{db['database']}"
    return create_engine(url, pool_pre_ping=True)

@st.cache_data(ttl=600) # Guarda en caché los datos por 10 minutos para que la app vuele
def cargar_desig_doc():
    """Ejecuta la consulta y devuelve el DataFrame"""
    engine = obtener_engine()
    consulta = "SELECT * FROM si_desig_doc;" # O el nombre exacto de tu tabla
    
    with engine.connect() as conn:
        df = pd.read_sql(consulta, conn)
    
    return df
'''