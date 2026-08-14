import pandas as pd
import mysql.connector
import os


# Conexión a MySQL
conexion = mysql.connector.connect(
    host="10.142.0.10",
    user="indicadores",
    password="ind_2022$Pa55",
    database="eUNSTAv3"
)


# Consulta
query = """
SELECT *
FROM si_inscriptos_7_anios
"""


# Obtener datos
df = pd.read_sql(query, conexion)

conexion.close()


# Guardar archivo
df.to_parquet(
    "../data/inscriptos_7_anios.parquet",
    index=False
)


print("Datos actualizados correctamente.")
print(f"Registros: {len(df)}")