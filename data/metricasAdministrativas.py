import pandas as pd
import streamlit as st
from data.metricasAcademicas import (
    cargar_datos_presupuesto,
    normalizar_texto_sede,
)
from utils.data_loader import cargar_datos_colaboradores

KEYWORDS_ACADEMICAS = [
    "FACULTAD", "FAC.", "CEOP", "C.E.O.P", "DEPTO FORMAC", "HUM. CRIST", 
    "FORM.HUM", "HUMANIDADES", "DERECHO", "ECONOMIA", "CURRHUMFOR", 
    "SALUD", "INGENIERIA", "CUC-",
    # variantes que aparecen en el Excel nominal (nombre completo, no
    # abreviatura de BD) para "Departamento de Formación Humanística"
    "HUMANISTIC", "HUMANÍSTIC",
]

# Traduce los nombres de área tal como figuran en el Excel nominal de
# colaboradores (data/colaboradores_admin.xlsx) al nombre oficial de
# "Sub unidad" usado en presupuesto.xlsx, para que ambas fuentes se puedan
# cruzar por el mismo nombre de área. Reemplaza al mapeo anterior, que
# traducía códigos internos de la BD (ej. "SER.TIC.SC-GOB") y ya no aplica.
#
# Pendiente de confirmar con el usuario (quedan sin mapear, ver fallback):
# "Mesa de entradas", "Gestión Administrativa", "SERVICIOS Educación Continua",
# "Tesorería", "Administración" (vs "Administración General").
MAPEO_SECCIONES_ADMIN = {
    "ADMINISTRACIÓN GENERAL": "Administracion General",
    "SERVICIOS TECNOLOGÍA DE LA INFORMACIÓN": "Serv. de Tecn. de la Inform.",
    "SERVICIOS INFRAESTRUCTURA Y MANTENIMIENTO": "Serv. de Infraest. y Manten.",
    "SERVICIOS DESARROLLO DE PERSONAS": "Serv. Desarrollo de Personas",
    "SERVICIOS ECONÓMICOS FINANCIEROS": "Serv. Econon. Fcieros.",
    "PLANEAMIENTO ECONÓMICO Y FINANCIERO": "Serv. Plan. Econ. Fciero.",
    "SERVICIOS CONTABILIDAD Y LIQUIDACIÓN DE HABERES": "Serv. Contab. y Liquid. Haberes",
    "SERVICIOS CONTABLE": "Serv. Contable",
    "COMPRAS": "Compras",
    "SERVICIOS ALUMNOS": "Serv. Alumnos",
    "SERVICIOS EDUCACIÓN A DISTANCIA": "Serv. Ed. A Distancia",
    "SERVICIOS DE EDUCACIÓN A DISTANCIA": "Serv. Ed. A Distancia",
    "SERVICIOS EXTENSIÓN Y VINCULACIÓN CON EL MEDIO": "Servicios de Extensión y Vinc. Con el medio",
    "SERVICIOS DE COMUNICACIÓN Y ESTRATEGIAS ONLINE": "Servicios de Comunicaciones y Estrategias On line",
    "SERVICIOS LEGALES Y TÉCNICOS": "Servicios Legales y Técnicos",
    "RECTORADO": "Rector",
    "VICERRECTORADO": "Vice-Rect. de Formación",
    "SECRETARIA GENERAL": "Secretaría General",
    "DIRECCIÓN DE PASTORAL": "Dir. Pastoral",
    "SERVICIOS DE PASTORAL": "Dir. Pastoral",
    "SERVICIOS ACADÉMICOS": "Serv. Académicos",
    "SERVICIOS CERTIFICACIÓN Y TÍTULOS": "Serv. Certif. y Títulos",
    "SERVICIOS BIBLIOTECAS": "Serv. Bibliotecas",
    "SERVICIOS EDITORIAL": "Serv. Editorial",
    "SERVICIOS ORIENTACIÓN VOCACIONAL Y EDUCATIVA": "Serv. Orientacion Vocacional Educat.",
    "SERVICIOS ASEGURAMIENTO DE LA CALIDAD": "Servicios de Aseguramiento de la Calidad",
    "SERVICIOS DE PROTOCOLO Y CEREMONIAL": "Serv. Protoc. Cerem. Gtion Espac. Comunes",
    "SERVICIOS DE INVESTIGACIÓN Y DESARROLLO": "Servicios de Investigación y Desarrollo",
    "SERVICIOS AUDITORIA OPERATIVA": "Serv. Auditoria Operativa",
    "DIRECCIÓN ACADÉMICA": "Dirección Academica",
    "SECRETARÍA ACADÉMICA": "Secretaría Académica",
    "PROMOCIÓN INSTITUCIONAL": "Promocion Institucional",
    "OP": "OPPDom. (Convento)",
}

# "Sub unidad" en presupuesto.xlsx trae variantes de tildes/puntuación para
# la misma oficina (ej. "Secretaria Academica" sin tildes y "Secretaría
# Académica" con tildes). Se normalizan a un único nombre canónico antes de
# filtrar/agrupar, para que el presupuesto de ambas variantes se sume junto
# y quede bajo la misma área que usan los colaboradores.
CANONICALIZAR_SUBUNIDAD_PRESUPUESTO = {
    "SECRETARIA ACADEMICA": "Secretaría Académica",
    "SECRETARÍA ACADÉMICA": "Secretaría Académica",
}


def canonicalizar_subunidad(nombre) -> str:
    """Normaliza una 'Sub unidad' de presupuesto a su nombre canónico, si aplica."""
    if not isinstance(nombre, str):
        return nombre
    limpio = nombre.strip()
    return CANONICALIZAR_SUBUNIDAD_PRESUPUESTO.get(limpio.upper(), limpio)

def normalizar_servicio_admin(seccion_bd: str) -> str | None:
    """
    Retorna la Subunidad del Excel si hay coincidencia en el mapeo.
    Si no hay coincidencia (y no es área académica), retorna el nombre original de la BD formateado.
    """
    if not isinstance(seccion_bd, str) or not seccion_bd.strip():
        return None

    s = seccion_bd.upper().strip()

    # 1. Filtro para descartar áreas puramente académicas
    if any(k in s for k in KEYWORDS_ACADEMICAS):
        return None

    # 2. Coincidencia exacta contra el mapeo (nombres completos del Excel
    # nominal, no fragmentos de código BD como antes). Se usa igualdad y no
    # "contiene" para evitar falsos positivos, ej. "RECTORADO" no debe
    # matchear dentro de "VICERRECTORADO".
    if s in MAPEO_SECCIONES_ADMIN:
        return MAPEO_SECCIONES_ADMIN[s]

    # 3. Si no coincide con el Excel, se mantiene el nombre original de la BD (limpio)
    nombre_bd_limpio = s.split(".SC")[0].split("-")[0].strip().title()
    return nombre_bd_limpio if nombre_bd_limpio else None


@st.cache_data(ttl=300)
def obtener_lista_areas_administrativas() -> list[str]:
    """
    Consolida las áreas del Excel de presupuesto y las áreas del Excel de colaboradores que no tuvieron coincidencia,
    generando una lista única y ordenada para el selector.
    """
    areas = set()

    # 1. Cargar Subunidades desde el Excel de Presupuesto
    df_presupuesto = cargar_datos_presupuesto()
    if not df_presupuesto.empty:
        df_presupuesto.columns = df_presupuesto.columns.str.strip()
        
        if "Categoria" in df_presupuesto.columns:
            df_admin = df_presupuesto[
                df_presupuesto["Categoria"].astype(str).str.upper().str.contains("ADMIN", na=False)
            ]
        else:
            df_admin = df_presupuesto

        col_sub = next(
            (c for c in df_admin.columns if "SUB" in c.upper() and "UNIDAD" in c.upper()), 
            "Sub unidad"
        )
        
        if col_sub in df_admin.columns:
            subunidades = (
                df_admin[col_sub]
                .dropna()
                .astype(str)
                .str.strip()
                .apply(canonicalizar_subunidad)
                .unique()
            )
            for sub in subunidades:
                if not any(k in sub.upper() for k in KEYWORDS_ACADEMICAS):
                    areas.add(sub)

    # 2. Cargar Áreas desde el Excel de Colaboradores (incluye los nombres no mapeados)
    try:
        df_colab = cargar_datos_colaboradores()
        if df_colab is not None and not df_colab.empty:
            col_servicio = "servicio" if "servicio" in df_colab.columns else "area"
            
            # Mapeamos o conservamos el nombre original de la BD
            areas_colab = (
                df_colab[col_servicio]
                .apply(normalizar_servicio_admin)
                .dropna()
                .unique()
            )
            
            for area in areas_colab:
                areas.add(area)
    except Exception as e:
        st.error(f"Error al consolidar áreas del Excel de colaboradores: {e}")

    lista_ordenada = sorted(list(areas))
    return ["Todas las Áreas"] + lista_ordenada


@st.cache_data(ttl=300)
def obtener_detalle_gastos_administrativo(
    nombre_area_app, sede="Todas las Sedes", mes="Anual (Ene-Dic)"
):
    """Desglose de gastos (Personal y Funcionamiento) desde el Presupuesto."""
    df = cargar_datos_presupuesto()
    if df.empty:
        return [], [], [], []

    try:
        df.columns = df.columns.str.strip()

        if "Categoria" in df.columns:
            df = df[df["Categoria"].astype(str).str.upper().str.contains("ADMIN", na=False)]

        if sede != "Todas las Sedes" and "Sede" in df.columns:
            sede_buscada = normalizar_texto_sede(sede)
            def coincide_sede(val_columna):
                val_norm = normalizar_texto_sede(str(val_columna))
                if "CONCEP" in sede_buscada or "CONCEO" in sede_buscada:
                    return "CONCEP" in val_norm or "CONCEO" in val_norm
                return sede_buscada in val_norm or val_norm in sede_buscada
            df = df[df["Sede"].apply(coincide_sede)]

        col_subunidad = next((c for c in df.columns if "SUB" in c.upper() and "UNIDAD" in c.upper()), "Sub unidad")
        df[col_subunidad] = df[col_subunidad].astype(str).str.strip().apply(canonicalizar_subunidad)

        if nombre_area_app != "Todas las Áreas":
            df_area = df[df[col_subunidad] == nombre_area_app.strip()].copy()
        else:
            df_area = df.copy()

        if df_area.empty:
            return [], [], [], []

        col_monto = "PRES. TOTAL"
        if mes != "Anual (Ene-Dic)":
            col_encontrada = next((c for c in df_area.columns if c.lower().strip() == mes.lower().strip()), None)
            if col_encontrada:
                col_monto = col_encontrada

        def limpiar_monto(val):
            if pd.isna(val):
                return 0.0
            if isinstance(val, (int, float)):
                return float(val)
            s = str(val).replace("$", "").strip()
            if "," in s and "." in s:
                s = s.replace(".", "").replace(",", ".")
            elif "," in s:
                s = s.replace(",", ".")
            try:
                return float(s)
            except Exception:
                return 0.0

        df_area["monto_limpio"] = df_area[col_monto].apply(limpiar_monto)

        col_tipo = next((c for c in df_area.columns if "DESC" in c.upper() and "TIPO" in c.upper()), None)
        if not col_tipo:
            col_tipo = next((c for c in df_area.columns if "TIPO" in c.upper()), "Descripción tipo")

        col_concepto = next((c for c in df_area.columns if "CONCEPTO" in c.upper()), "Concepto")

        # Personal
        df_personal = df_area[df_area[col_tipo].astype(str).str.upper().str.contains("PERS", na=False)]
        grp_personal = df_personal.groupby(col_concepto)["monto_limpio"].sum().sort_values(ascending=False)
        grp_personal = grp_personal[grp_personal > 0]

        # Funcionamiento
        df_func = df_area[df_area[col_tipo].astype(str).str.upper().str.contains("FUNC", na=False)]
        grp_func = df_func.groupby(col_concepto)["monto_limpio"].sum().sort_values(ascending=False).head(5)
        grp_func = grp_func[grp_func > 0]

        return grp_personal.index.tolist(), grp_personal.values.tolist(), grp_func.index.tolist(), grp_func.values.tolist()

    except Exception as e:
        st.error(f"Error al obtener detalle de gastos: {e}")
        return [], [], [], []


@st.cache_data(ttl=300)
def calcular_kpis_administrativos(
    nombre_area="Todas las Áreas",
    sede="Todas las Sedes",
    mes="Anual (Ene-Dic)",
):
    """Calcula la cantidad total de colaboradores y el Presupuesto, ambos desde Excel."""
    cant_colaboradores = 0
    presupuesto_total = 0.0

    # 1. CÁLCULO DE COLABORADORES
    try:
        df_colab = cargar_datos_colaboradores()
        if df_colab is not None and not df_colab.empty:
            col_servicio = "servicio" if "servicio" in df_colab.columns else "area"
            df_colab["sub_unidad_norm"] = df_colab[col_servicio].apply(normalizar_servicio_admin)
            df_colab = df_colab[df_colab["sub_unidad_norm"].notnull()]

            if sede != "Todas las Sedes" and "sede" in df_colab.columns and df_colab["sede"].notna().any():
                sede_buscada = normalizar_texto_sede(sede)
                def coincide_sede(val_col):
                    val_norm = normalizar_texto_sede(str(val_col))
                    if "CONCEP" in sede_buscada or "CONCEO" in sede_buscada:
                        return "CONCEP" in val_norm or "CONCEO" in val_norm
                    return sede_buscada in val_norm or val_norm in sede_buscada
                df_colab = df_colab[df_colab["sede"].apply(coincide_sede)]

            if nombre_area != "Todas las Áreas":
                df_colab = df_colab[
                    df_colab["sub_unidad_norm"].astype(str).str.strip().str.upper() == nombre_area.strip().upper()
                ]

            if not df_colab.empty and "total" in df_colab.columns:
                cant_colaboradores = int(df_colab["total"].sum())
    except Exception as e:
        st.error(f"Error al calcular colaboradores administrativos: {e}")

    # 2. CÁLCULO DE PRESUPUESTO
    df = cargar_datos_presupuesto()
    if not df.empty:
        df.columns = df.columns.str.strip()

        df_admin = df[df["Categoria"].astype(str).str.upper().str.contains("ADMIN", na=False)].copy()

        if sede != "Todas las Sedes" and "Sede" in df_admin.columns:
            sede_buscada = normalizar_texto_sede(sede)
            def coincide_sede(val_columna):
                val_norm = normalizar_texto_sede(str(val_columna))
                if "CONCEP" in sede_buscada or "CONCEO" in sede_buscada:
                    return "CONCEP" in val_norm or "CONCEO" in val_norm
                return sede_buscada in val_norm or val_norm in sede_buscada
            df_admin = df_admin[df_admin["Sede"].apply(coincide_sede)]

        if nombre_area != "Todas las Áreas":
            col_sub = next((c for c in df_admin.columns if "SUB" in c.upper() and "UNIDAD" in c.upper()), "Sub unidad")
            df_admin[col_sub] = df_admin[col_sub].astype(str).str.strip().apply(canonicalizar_subunidad)
            df_admin = df_admin[df_admin[col_sub] == nombre_area.strip()]

        if not df_admin.empty:
            col_monto = "PRES. TOTAL"
            if mes != "Anual (Ene-Dic)":
                col_encontrada = next((c for c in df_admin.columns if c.lower().strip() == mes.lower().strip()), None)
                if col_encontrada:
                    col_monto = col_encontrada

            def limpiar_monto(val):
                if pd.isna(val):
                    return 0.0
                if isinstance(val, (int, float)):
                    return float(val)
                s = str(val).replace("$", "").strip()
                if "," in s and "." in s:
                    s = s.replace(".", "").replace(",", ".")
                elif "," in s:
                    s = s.replace(",", ".")
                try:
                    return float(s)
                except Exception:
                    return 0.0

            presupuesto_total = df_admin[col_monto].apply(limpiar_monto).sum()

    return cant_colaboradores, presupuesto_total


def formatear_monto_millones(monto):
    """Formatea el monto completo en pesos."""
    try:
        val_float = float(monto)
        return f"$ {val_float:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "$ 0"