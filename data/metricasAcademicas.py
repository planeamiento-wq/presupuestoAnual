import pandas as pd
import streamlit as st
from utils.data_loader import cargar_datos_presupuesto, cargar_datos_colaboradores
import unicodedata

RUTA_ALUMNOS_ACTIVOS = "data/alumnos_activos_facultad.parquet"
RUTA_DOCENTES = "data/docentes_resumen.parquet"

def normalizar_texto_sede(texto):
    """Quita acentos, convierte a mayúsculas y limpia espacios para hacer comparaciones tolerantes."""
    if not isinstance(texto, str) or not texto:
        return ""
    # Elimina tildes y diacríticos (ej: CONCEPCIÓN -> CONCEPCION)
    texto_sin_tildes = "".join(
        c
        for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )
    return texto_sin_tildes.upper().strip()


def normalizar_facultad(nombre):
  """Mapea las unidades académicas reconociendo excepciones como CEOP y DFHC."""
  if not isinstance(nombre, str) or not nombre:
    return None

  n = nombre.upper().strip()

  # Excepciones específicas según la base de datos
  if (
      "FILOSOF" in n or "TEOLOG" in n or "CEOP" in n or "CENTRO DE ESTUDIOS" in n
  ):
    return "CEOP"
  elif (
      "DFHC" in n
      or "DEPTO.FORM" in n
      or "FORM.HUM" in n
      or "HUM.CRIST" in n
      or "FORMAC" in n
      or "CRISTIANA" in n
  ) and not (
      "HUMAN." in n or "FAC. HUMANIDADES" in n or "FACULTAD DE HUMANIDADES" in n
  ):
    return "Dpto. de Formación Humanística"
  elif "ECON" in n or "ADM" in n or "FAC. ECON" in n:
    return "Facultad de Economía y Administración"
  elif (
      "JURID" in n
      or "JPYS" in n
      or "POLIT" in n
      or "SOC" in n
      or "DERECHO" in n
      or "FAC. CS JURID" in n
  ):
    return "Facultad de Ciencias Jurídicas"
  elif (
      "INGENIER" in n or "INGENIÉR" in n or "INGENIE." in n or "FAC. INGENIERIA" in n
  ):
    return "Facultad de Ingeniería"
  elif "SALUD" in n or "MEDICIN" in n or "FAC. CS. SALUD" in n:
    return "Facultad de Ciencias de la Salud"
  elif "HUMAN." in n or "HUMANID" in n:
    return "Facultad de Humanidades"
  else:
    return None


@st.cache_data(ttl=300)
def obtener_alumnos_activos_por_facultad(sede="Todas las Sedes"):
    """Devuelve el resumen por facultad y el total dinámico seguro considerando el filtro tolerante de sede.

    Lee el resultado pre-calculado por actualizador/actualizador.py (misma
    consulta que antes se ejecutaba en vivo) en vez de conectarse a la base.
    """
    try:
        df = pd.read_parquet(RUTA_ALUMNOS_ACTIVOS)
        if df is None or df.empty:
            return {}, 0

        # Blindaje de nulos en 'sede' y 'facultad'
        df["sede"] = df["sede"].fillna("").astype(str)
        df["facultad"] = df["facultad"].fillna("").astype(str)

        # Filtro Tolerante por Sede
        if sede != "Todas las Sedes":
            sede_buscada = normalizar_texto_sede(sede)

            def coincide_sede(val_columna):
                val_norm = normalizar_texto_sede(str(val_columna))
                if "CONCEP" in sede_buscada or "CONCEO" in sede_buscada:
                    return "CONCEP" in val_norm or "CONCEO" in val_norm
                return sede_buscada in val_norm or val_norm in sede_buscada

            df = df[df["sede"].apply(coincide_sede)]

        total_real_absoluto = (
            int(df["activos"].sum()) if not df.empty else 0
        )

        # Mapeo por facultad oficial
        df["facultad_oficial"] = df["facultad"].apply(normalizar_facultad)
        df_mapeado = df.dropna(subset=["facultad_oficial"])

        resumen = (
            df_mapeado.groupby("facultad_oficial")["activos"].sum().to_dict()
        )

        return resumen, total_real_absoluto

    except FileNotFoundError:
        st.error(
            f"⚠️ No se encontró '{RUTA_ALUMNOS_ACTIVOS}'. Ejecutá"
            " actualizador/actualizador.py para generar los datos."
        )
        return {}, 0
    except Exception as e:
        st.error(f"Error al procesar el cálculo dinámico de Alumnos: {e}")
        return {}, 0


@st.cache_data(ttl=300)
def obtener_colaboradores_por_area(sede="Todas las Sedes"):
    """Consulta los colaboradores de unidades académicas filtrando por 'FAC.', Formación Humanística y C.E.O.P."""

    # Definimos la función de mapeo al inicio para que esté accesible en todo el scope
    def mapear_colaborador_academico(area_nombre):
        if not isinstance(area_nombre, str) or not area_nombre:
            return None

        a = area_nombre.upper().strip()

        # Caso 1: Dpto. de Formación Humanística
        # (cubre tanto las abreviaturas que traía la BD -DEPTO.FORM, HUM.CRIST-
        # como el nombre completo tal cual figura en el Excel nominal)
        if any(
            k in a
            for k in [
                "DEPTO FORMAC",
                "HUM. CRIST",
                "HUM.CRIST",
                "FORM.HUM",
                "DEPTO.FORM",
                "HUMANISTIC",
                "HUMANÍSTIC",
            ]
        ):
            return "Dpto. de Formación Humanística"

        # Caso 2: C.E.O.P.
        if "C.E.O.P" in a or "CEOP" in a:
            return "CEOP"

        # Caso 3: Facultades que empiezan con 'FAC.'
        if a.startswith("FAC.") or "FACULTAD" in a:
            return normalizar_facultad(a)

        # Áreas administrativas no académicas se ignoran
        return None

    # Lee y agrupa el Excel nominal de colaboradores (utils/data_loader.py).
    # Ya no depende de actualizador/actualizador.py ni de la BD en vivo.
    try:
        df = cargar_datos_colaboradores()
        if df is None or df.empty:
            return {}

        if (
            sede != "Todas las Sedes"
            and "sede" in df.columns
            and df["sede"].notna().any()
        ):
            sede_buscada = normalizar_texto_sede(sede)

            def coincide_sede(val_columna):
                val_norm = normalizar_texto_sede(str(val_columna))
                if "CONCEP" in sede_buscada or "CONCEO" in sede_buscada:
                    return "CONCEP" in val_norm or "CONCEO" in val_norm
                return sede_buscada in val_norm or val_norm in sede_buscada

            df = df[df["sede"].apply(coincide_sede)]

        if df.empty:
            return {}

        df["facultad_oficial"] = df["area"].apply(mapear_colaborador_academico)
        df_mapeado = df.dropna(subset=["facultad_oficial"])
        return df_mapeado.groupby("facultad_oficial")["total"].sum().to_dict()

    except Exception as ex:
        st.error(f"Error al procesar colaboradores: {ex}")
        return {}

@st.cache_data(ttl=300)
def obtener_presupuesto_por_facultad(
    sede="Todas las Sedes", mes="Anual (Ene-Dic)"
):
    """Carga y calcula el Presupuesto Total ($ Disponible) filtrando estrictamente por Unidad, Subunidad y Mes."""
    df = cargar_datos_presupuesto()
    if df.empty:
        return {}

    try:
        # 1. Filtro por Categoria == 'Académico'
        if "Categoria" in df.columns:
            df = df[
                df["Categoria"]
                .astype(str)
                .str.upper()
                .str.contains("ACAD", na=False)
            ]

        # 2. Filtro Tolerante por Sede (Maneja CONCEPCIÓN, CONCEOPCION, etc.)
        if sede != "Todas las Sedes" and "Sede" in df.columns:
            sede_buscada = normalizar_texto_sede(sede)

            def coincide_sede(val_columna):
                val_norm = normalizar_texto_sede(str(val_columna))
                if "CONCEP" in sede_buscada or "CONCEO" in sede_buscada:
                    return "CONCEP" in val_norm or "CONCEO" in val_norm
                return sede_buscada in val_norm or val_norm in sede_buscada

            df = df[df["Sede"].apply(coincide_sede)]

        # 2b. NUEVO: Filtro por Mes
        if mes != "Anual (Ene-Dic)":
            col_mes = next(
                (
                    c
                    for c in df.columns
                    if any(
                        k in c.upper()
                        for k in ["MES", "PERIODO", "FECHA", "MES_NOMBRE"]
                    )
                ),
                None,
            )
            if col_mes:
                df = df[
                    df[col_mes].astype(str).str.upper() == str(mes).upper()
                ]

        # 3. Detectar columna de Monto
        posibles_columnas_monto = [
            "PRES. TOTAL",
            "PRESUPUESTO",
            "MONTO",
            "TOTAL",
            "IMPORTE",
            "DISPONIBLE",
            "CREDITO",
            "PRES_TOTAL",
            "PRES TOTAL",
        ]
        col_monto = next(
            (
                c
                for c in df.columns
                if any(k in c.upper() for k in posibles_columnas_monto)
            ),
            None,
        )

        if not col_monto:
            cols_num = df.select_dtypes(include=["number"]).columns
            if len(cols_num) > 0:
                col_monto = cols_num[-1]

        if not col_monto:
            return {}

        # 4. Limpieza de montos
        def limpiar_numero(val):
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
            except:
                return 0.0

        df["monto_limpio"] = df[col_monto].apply(limpiar_numero)

        # Detectar columnas exactas
        col_unidad = next(
            (
                c
                for c in df.columns
                if "UNIDAD" in c.upper() and "SUB" not in c.upper()
            ),
            None,
        )
        col_subunidad = next(
            (
                c
                for c in df.columns
                if "SUB" in c.upper() and "UNIDAD" in c.upper()
            ),
            None,
        )

        # 5. Mapeo Quirúrgico
        def extraer_unidad_oficial(row):
            txt_unidad = (
                str(row[col_unidad]).upper().strip()
                if col_unidad and pd.notna(row[col_unidad])
                else ""
            )
            txt_subunidad = (
                str(row[col_subunidad]).upper().strip()
                if col_subunidad and pd.notna(row[col_subunidad])
                else ""
            )

            # CASO 1: Dpto. de Formación Humanística
            # Solo si la subunidad es explícitamente Depto.Form.Hum.Crist. / Formación Humanística
            if any(
                k in txt_subunidad
                for k in [
                    "DEPTO.FORM",
                    "HUM.CRIST",
                    "FORM.HUM",
                    "HUMANISTICA",
                    "HUMANÍSTICA",
                ]
            ):
                return "Dpto. de Formación Humanística"

            # CASO 2: CEOP (Directo por columna Unidad)
            if "CEOP" in txt_unidad or "CENTRO DE ESTUDIOS" in txt_unidad:
                return "CEOP"

            # CASO 3: Las demás Facultades
            # Primero probamos clasificar por la columna Unidad
            fac = normalizar_facultad(txt_unidad)
            if fac:
                return fac

            return None

        df["facultad_oficial"] = df.apply(extraer_unidad_oficial, axis=1)

        # 6. Agrupar y sumar
        df_academico = df.dropna(subset=["facultad_oficial"])
        resumen = (
            df_academico.groupby("facultad_oficial")["monto_limpio"]
            .sum()
            .to_dict()
        )

        return resumen

    except Exception as e:
        st.error(f"Error al procesar el presupuesto: {e}")
        return {}

@st.cache_data(ttl=300)
def obtener_metricas_docentes(sede="Todas las Sedes"):
    """Calcula docentes únicos globales, total de horas y desglose formateado por facultad."""
    try:
        df = pd.read_parquet(RUTA_DOCENTES)
        if df is None or df.empty:
            return {}, "0", "0"

        # Filtro de sede si la columna estuviese presente
        if (
            sede != "Todas las Sedes"
            and "sede" in df.columns
            and df["sede"].notna().any()
        ):
            sede_buscada = normalizar_texto_sede(sede)

            def coincide_sede(val_columna):
                val_norm = normalizar_texto_sede(str(val_columna))
                if "CONCEP" in sede_buscada or "CONCEO" in sede_buscada:
                    return "CONCEP" in val_norm or "CONCEO" in val_norm
                return sede_buscada in val_norm or val_norm in sede_buscada

            df = df[df["sede"].apply(coincide_sede)]

        if df.empty:
            return {}, "0", "0"

        # 1. Totales Globales
        total_docentes_unicos = df["id_docente"].nunique()
        total_horas = df["horas_docente"].sum()

        # 2. Mapeo usando la función común normalizar_facultad
        df["facultad_oficial"] = df["unidad"].apply(normalizar_facultad)
        df_mapeado = df.dropna(subset=["facultad_oficial"])

        # Agrupaciones por facultad
        docentes_por_facultad = (
            df_mapeado.groupby("facultad_oficial")["id_docente"]
            .nunique()
            .to_dict()
        )
        horas_por_facultad = (
            df_mapeado.groupby("facultad_oficial")["horas_docente"]
            .sum()
            .to_dict()
        )

        # Formateo de strings con puntos separadores de miles
        dict_docentes = {}
        for fac, cant in docentes_por_facultad.items():
            hs = horas_por_facultad.get(fac, 0)
            dict_docentes[fac] = {
                "doc": f"{cant:,}".replace(",", "."),
                "hs": f"{hs:,.0f}".replace(",", "."),
            }

        doc_total_str = f"{total_docentes_unicos:,}".replace(",", ".")
        hs_total_str = f"{total_horas:,.0f}".replace(",", ".")

        return dict_docentes, doc_total_str, hs_total_str

    except FileNotFoundError:
        st.error(
            f"⚠️ No se encontró '{RUTA_DOCENTES}'. Ejecutá"
            " actualizador/actualizador.py para generar los datos."
        )
        return {}, "0", "0"
    except Exception as e:
        st.error(f"Error al procesar las métricas de docentes: {e}")
        return {}, "0", "0"

@st.cache_data(ttl=300)
def obtener_detalle_gastos_UA(
    nombre_unidad_app, sede="Todas las Sedes", mes="Anual (Ene-Dic)"
):
    """Filtra los gastos de personal y funcionamiento de una unidad específica

    usando la normalización existente.
    """
    df = cargar_datos_presupuesto()
    if df.empty:
        return [], [], [], []

    try:
        # 0. Limpieza de espacios en los nombres de las columnas
        df.columns = df.columns.str.strip()

        # 1. Filtro por Categoria == 'Académico'
        if "Categoria" in df.columns:
            df = df[
                df["Categoria"]
                .astype(str)
                .str.upper()
                .str.contains("ACAD", na=False)
            ]

        # 2. Filtro Tolerante por Sede
        if sede != "Todas las Sedes" and "Sede" in df.columns:
            sede_buscada = normalizar_texto_sede(sede)

            def coincide_sede(val_columna):
                val_norm = normalizar_texto_sede(str(val_columna))
                if "CONCEP" in sede_buscada or "CONCEO" in sede_buscada:
                    return "CONCEP" in val_norm or "CONCEO" in val_norm
                return sede_buscada in val_norm or val_norm in sede_buscada

            df = df[df["Sede"].apply(coincide_sede)]

        # 3. Mapeo de Unidad y filtro especial de Subunidad
        col_unidad = next(
            (
                c
                for c in df.columns
                if "UNIDAD" in c.upper() and "SUB" not in c.upper()
            ),
            None,
        )
        col_subunidad = next(
            (
                c
                for c in df.columns
                if "SUB" in c.upper() and "UNIDAD" in c.upper()
            ),
            None,
        )

        def extraer_unidad_oficial(row):
            txt_unidad = (
                str(row[col_unidad]).upper().strip()
                if col_unidad and pd.notna(row[col_unidad])
                else ""
            )
            txt_subunidad = (
                str(row[col_subunidad]).upper().strip()
                if col_subunidad and pd.notna(row[col_subunidad])
                else ""
            )

            # Filtro fino para Dpto. de Formación Humanística
            if any(
                k in txt_subunidad
                for k in [
                    "DEPTO.FORM",
                    "HUM.CRIST",
                    "FORM.HUM",
                    "HUMANISTICA",
                    "HUMANÍSTICA",
                ]
            ):
                return "Dpto. de Formación Humanística"

            if "CEOP" in txt_unidad or "CENTRO DE ESTUDIOS" in txt_unidad:
                return "CEOP"

            return normalizar_facultad(txt_unidad)

        df["facultad_oficial"] = df.apply(extraer_unidad_oficial, axis=1)

        # Filtramos estrictamente por la unidad seleccionada en la App
        df_unidad = df[df["facultad_oficial"] == nombre_unidad_app].copy()
        if df_unidad.empty:
            return [], [], [], []

        # 4. Determinar columna de monto según el mes seleccionado
        col_monto = "PRES. TOTAL"
        if mes != "Anual (Ene-Dic)":
            col_encontrada = next(
                (
                    c
                    for c in df_unidad.columns
                    if c.lower().strip() == mes.lower().strip()
                ),
                None,
            )
            if col_encontrada:
                col_monto = col_encontrada

        # Clean-up numérico
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

        df_unidad["monto_limpio"] = df_unidad[col_monto].apply(limpiar_monto)

        # --- DETECCIÓN CORRECTA DE LA COLUMNA DE TIPO DE GASTO ---
        # Priorizamos 'Descripción tipo' / 'DESCRIPCION' para no confundir con la columna 'Tipo' (EGRESOS/INGRESOS)
        col_tipo = next(
            (
                c
                for c in df_unidad.columns
                if "DESC" in c.upper() and "TIPO" in c.upper()
            ),
            None,
        )
        if not col_tipo:
            col_tipo = next(
                (c for c in df_unidad.columns if "TIPO" in c.upper()),
                "Descripción tipo",
            )

        col_concepto = next(
            (c for c in df_unidad.columns if "CONCEPTO" in c.upper()),
            "Concepto",
        )

        # --- A. GASTOS DE PERSONAL (Dona) ---
        df_personal = df_unidad[
            df_unidad[col_tipo]
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

        # --- B. GASTOS DE FUNCIONAMIENTO (Barras) ---
        df_func = df_unidad[
            df_unidad[col_tipo]
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
        st.error(f"Error al obtener el detalle de gastos de la unidad: {e}")
        return [], [], [], []