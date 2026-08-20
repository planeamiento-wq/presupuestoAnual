import pandas as pd
import streamlit as st
from data.metricasAcademicas import cargar_datos_presupuesto, normalizar_texto_sede


@st.cache_data(ttl=300)
def obtener_lista_areas_administrativas():
    """Devuelve el listado único de Subunidades para la categoría Administrativo."""
    df = cargar_datos_presupuesto()
    if df.empty:
        return ["Todas las Áreas"]

    df.columns = df.columns.str.strip()

    df_admin = df[
        df["Categoria"].astype(str).str.upper().str.contains("ADMIN", na=False)
    ]
    col_sub = next(
        (c for c in df.columns if "SUB" in c.upper() and "UNIDAD" in c.upper()),
        "Sub unidad",
    )

    areas = (
        df_admin[col_sub].dropna().astype(str).str.strip().unique().tolist()
    )
    areas.sort()
    return ["Todas las Áreas"] + areas


@st.cache_data(ttl=300)
def obtener_detalle_gastos_administrativo(
    nombre_area_app, sede="Todas las Sedes", mes="Anual (Ene-Dic)"
):
    """Filtra y devuelve el desglose de gastos (Personal y Funcionamiento)

    para un Área / Servicio / Subunidad Administrativa específica.
    """
    df = cargar_datos_presupuesto()
    if df.empty:
        return [], [], [], []

    try:
        df.columns = df.columns.str.strip()

        # 1. Filtro estricto por Categoria == 'Administrativo'
        if "Categoria" in df.columns:
            df = df[
                df["Categoria"]
                .astype(str)
                .str.upper()
                .str.contains("ADMIN", na=False)
            ]

        # 2. Filtro por Sede
        if sede != "Todas las Sedes" and "Sede" in df.columns:
            sede_buscada = normalizar_texto_sede(sede)

            def coincide_sede(val_columna):
                val_norm = normalizar_texto_sede(str(val_columna))
                if "CONCEP" in sede_buscada or "CONCEO" in sede_buscada:
                    return "CONCEP" in val_norm or "CONCEO" in val_norm
                return sede_buscada in val_norm or val_norm in sede_buscada

            df = df[df["Sede"].apply(coincide_sede)]

        # 3. Filtro por Subunidad / Área
        col_subunidad = next(
            (
                c
                for c in df.columns
                if "SUB" in c.upper() and "UNIDAD" in c.upper()
            ),
            "Sub unidad",
        )

        if nombre_area_app != "Todas las Áreas":
            df_area = df[
                df[col_subunidad].astype(str).str.strip()
                == nombre_area_app.strip()
            ].copy()
        else:
            df_area = df.copy()

        if df_area.empty:
            return [], [], [], []

        # 4. Determinar columna de monto según el mes
        col_monto = "PRES. TOTAL"
        if mes != "Anual (Ene-Dic)":
            col_encontrada = next(
                (
                    c
                    for c in df_area.columns
                    if c.lower().strip() == mes.lower().strip()
                ),
                None,
            )
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

        # Detectar columnas de Tipo y Concepto
        col_tipo = next(
            (
                c
                for c in df_area.columns
                if "DESC" in c.upper() and "TIPO" in c.upper()
            ),
            None,
        )
        if not col_tipo:
            col_tipo = next(
                (c for c in df_area.columns if "TIPO" in c.upper()),
                "Descripción tipo",
            )

        col_concepto = next(
            (c for c in df_area.columns if "CONCEPTO" in c.upper()),
            "Concepto",
        )

        # Gastos de Personal
        df_personal = df_area[
            df_area[col_tipo]
            .astype(str)
            .str.upper()
            .str.contains("PERS", na=False)
        ]
        grp_personal = (
            df_personal.groupby(col_concepto)["monto_limpio"]
            .sum()
            .sort_values(ascending=False)
        )
        grp_personal = grp_personal[grp_personal > 0]

        labels_personal = grp_personal.index.tolist()
        valores_personal = grp_personal.values.tolist()

        # Gastos de Funcionamiento
        df_func = df_area[
            df_area[col_tipo]
            .astype(str)
            .str.upper()
            .str.contains("FUNC", na=False)
        ]
        grp_func = (
            df_func.groupby(col_concepto)["monto_limpio"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
        )
        grp_func = grp_func[grp_func > 0]

        cat_func = grp_func.index.tolist()
        val_func = grp_func.values.tolist()

        return labels_personal, valores_personal, cat_func, val_func

    except Exception as e:
        st.error(f"Error al obtener el detalle de gastos administrativos: {e}")
        return [], [], [], []

@st.cache_data(ttl=300)
def calcular_kpis_administrativos(
    nombre_area="Todas las Áreas",
    sede="Todas las Sedes",
    mes="Anual (Ene-Dic)",
):
    """Calcula el total de colaboradores administrativos y el presupuesto acumulado/disponible."""
    df = cargar_datos_presupuesto()
    if df.empty:
        return 0, 0.0

    df.columns = df.columns.str.strip()

    # 1. Filtro estricto por Categoria 'Administrativo'
    df_admin = df[
        df["Categoria"].astype(str).str.upper().str.contains("ADMIN", na=False)
    ].copy()

    # 2. Filtro por Sede
    if sede != "Todas las Sedes" and "Sede" in df_admin.columns:
        sede_buscada = normalizar_texto_sede(sede)

        def coincide_sede(val_columna):
            val_norm = normalizar_texto_sede(str(val_columna))
            if "CONCEP" in sede_buscada or "CONCEO" in sede_buscada:
                return "CONCEP" in val_norm or "CONCEO" in val_norm
            return sede_buscada in val_norm or val_norm in sede_buscada

        df_admin = df_admin[df_admin["Sede"].apply(coincide_sede)]

    # 3. Filtro por Subunidad / Área
    if nombre_area != "Todas las Áreas":
        col_sub = next(
            (
                c
                for c in df_admin.columns
                if "SUB" in c.upper() and "UNIDAD" in c.upper()
            ),
            "Sub unidad",
        )
        df_admin = df_admin[
            df_admin[col_sub].astype(str).str.strip() == nombre_area.strip()
        ]

    if df_admin.empty:
        return 0, 0.0

    # --- CÁLCULO DE COLABORADORES ---
    # Contamos la cantidad de registros asociados a 'Gastos Personal'
    col_tipo = next(
        (
            c
            for c in df_admin.columns
            if "DESC" in c.upper() and "TIPO" in c.upper()
        ),
        "Descripción tipo",
    )
    cant_colaboradores = len(
        df_admin[
            df_admin[col_tipo]
            .astype(str)
            .str.upper()
            .str.contains("PERS", na=False)
        ]
    )

    # --- CÁLCULO DE PRESUPUESTO ---
    col_monto = "PRES. TOTAL"
    if mes != "Anual (Ene-Dic)":
        col_encontrada = next(
            (
                c
                for c in df_admin.columns
                if c.lower().strip() == mes.lower().strip()
            ),
            None,
        )
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
    """Formatea montos grandes a formato legible (ej: $ 24.506 M o $ 850 K)."""
    if monto >= 1_000_000_000:
        return f"$ {monto / 1_000_000_000:,.2f} B".replace(",", ".")
    elif monto >= 1_000_000:
        return f"$ {monto / 1_000_000:,.1f} M".replace(",", ".")
    elif monto >= 1_000:
        return f"$ {monto / 1_000:,.1f} K".replace(",", ".")
    else:
        return f"$ {monto:,.0f}".replace(",", ".")