import os

import pandas as pd
import mysql.connector
from dotenv import load_dotenv

# Busca un archivo .env en la carpeta actual o en carpetas superiores
# (ver actualizador/.env.example para las variables necesarias)
#load_dotenv()

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

DB_HOST = os.environ["DB_HOST"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_NAME = os.environ.get("DB_NAME", "eUNSTAv3")

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# Consultas: deben coincidir exactamente con las que hacían las páginas
# contra la base en vivo (utils/conexion.py). Si esas queries cambian,
# actualizar también acá.
QUERIES = {
    "inscriptos_7_anios.parquet": """
        SELECT *
        FROM si_inscriptos_7_anios
    """,
    "alumnos_activos_facultad.parquet": """
        SELECT
            pos.sede,
            pos.facultad,
            COUNT(DISTINCT pos.id_alumno) AS activos
        FROM (
            SELECT sede, unidad_largo AS facultad, id_alumno FROM si_inscriptos_new
            UNION
            SELECT sede, unidad AS facultad, id_alumno FROM si_reinscriptos
        ) pos
        LEFT JOIN (
            SELECT id_alumno FROM si_cancela_matricula
            UNION
            SELECT id_alumno FROM si_cancelados_reinscriptos
        ) neg ON pos.id_alumno = neg.id_alumno
        WHERE neg.id_alumno IS NULL
        GROUP BY pos.sede, pos.facultad
    """,
    "docentes_resumen.parquet": """
        SELECT 
            unidad,
            id_docente,
            SUM(horas) AS horas_docente
        FROM si_desig_doc
        WHERE id_estado = 1
        GROUP BY unidad, id_docente
    """,
}

# La consulta de colaboradores por área tiene una variante con "sede" y un
# fallback sin esa columna, tal como hacía la app en vivo.
QUERY_COLABORADORES_CON_SEDE = """
    SELECT TRIM(seccion_nombre) AS area, sede, COUNT(*) AS total
    FROM si_empleados
    GROUP BY TRIM(seccion_nombre), sede
"""
QUERY_COLABORADORES_SIN_SEDE = """
    SELECT TRIM(seccion_nombre) AS area, COUNT(*) AS total
    FROM si_empleados
    GROUP BY TRIM(seccion_nombre)
"""


def exportar_colaboradores(conexion):
    try:
        df = pd.read_sql(QUERY_COLABORADORES_CON_SEDE, conexion)
    except Exception:
        df = pd.read_sql(QUERY_COLABORADORES_SIN_SEDE, conexion)
        df["sede"] = None
    return df


def main():
    conexion = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )

    try:
        for nombre_archivo, query in QUERIES.items():
            df = pd.read_sql(query, conexion)
            ruta = os.path.join(DATA_DIR, nombre_archivo)
            df.to_parquet(ruta, index=False)
            print(f"{nombre_archivo}: {len(df)} registros")

        df_colaboradores = exportar_colaboradores(conexion)
        ruta_colaboradores = os.path.join(DATA_DIR, "colaboradores_area.parquet")
        df_colaboradores.to_parquet(ruta_colaboradores, index=False)
        print(f"colaboradores_area.parquet: {len(df_colaboradores)} registros")
    finally:
        conexion.close()

    print("Datos actualizados correctamente.")


if __name__ == "__main__":
    main()
