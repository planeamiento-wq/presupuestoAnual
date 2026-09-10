import streamlit as st

from styles.styles import cargar_estilo
from components.header import crear_header
from components.footer import crear_footer
from components.kpiCard import crear_kpi, crear_kpi_html
from components.barraProgreso import crear_barra
from components.card import abrir_card, cerrar_card
from components.graficoConsolidado import crear_grafico_consolidado
from components.tablaConsolidado import crear_tabla_consolidado
from components.mayoresConceptos import crear_grafico_mayores_conceptos

# IMPORTAMOS EL CARGADOR DE DATOS REALES
from utils.data_loader import cargar_datos_presupuesto

def mostrar_resumen():
    # Llamo los componentes y estilo
    cargar_estilo()

    crear_header(
        "RESUMEN EJECUTIVO",
        "Seguimiento del presupuesto institucional"
    )

    # =========================================================
    # 1. CARGA DE DATOS Y FILTROS GLOBALES DINÁMICOS
    # =========================================================
    df = cargar_datos_presupuesto()
    
    if df.empty:
        st.warning("⚠️ No se encontraron datos para procesar. Verifica tu archivo 'data/presupuesto.xlsx'.")
        return

    # Extraemos dinámicamente las columnas de meses/totales reales que vienen en el Excel
    columnas_df = list(df.columns)
    if 'Concepto' in columnas_df:
        idx_concepto = columnas_df.index('Concepto')
        meses_disponibles = [col.strip() for col in columnas_df[idx_concepto + 1:]]
    else:
        meses_disponibles = [col.strip() for col in df.columns if col.strip() not in ['Sede', 'Tipo', 'Descripción tipo', 'Unidad', 'Sub unidad', 'Categoria', 'Concepto']]

    # Estructura de 3 columnas para empujar los filtros a la derecha y hacerlos cortos
    col_vacia, col_f1, col_f2 = st.columns([4.0, 1.5, 1.5])
    
    with col_f1:
        lista_sedes = ["Todas las Sedes"] + sorted(list(df['Sede'].unique()))
        sede_seleccionada = st.selectbox("Sede:", lista_sedes)
        
    with col_f2:
        # Buscamos 'PRES. TOTAL' de forma inteligente mapeando espacios libres
        indice_defecto = 0
        for i, m in enumerate(meses_disponibles):
            if "PRES. TOTAL" in m.upper():
                indice_defecto = i
                break
        
        mes_seleccionado = st.selectbox("Período:", options=meses_disponibles, index=indice_defecto)

    st.markdown("<br>", unsafe_allow_html=True)

    # DECLARACIÓN DE VARIABLES DE FILTRADO (Evita NameError en las funciones de abajo)
    df_filtrado = df.copy()
    if sede_seleccionada != "Todas las Sedes":
        df_filtrado = df_filtrado[df_filtrado['Sede'] == sede_seleccionada]

    # Mapeamos la columna real del DataFrame original para evitar el KeyError
    col_mes = df.columns[columnas_df.index(df.columns[meses_disponibles.index(mes_seleccionado) + (columnas_df.index('Concepto') + 1)])]

    # =========================================================
    # 2. MOTOR MATEMÁTICO REAL 
    # =========================================================
    
    def normalizar_texto(texto):
        if not isinstance(texto, str):
            return ""
        import unicodedata
        texto_norm = "".join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
        return texto_norm.upper().strip()

    def sum_concepto_robusto(termino_busqueda):
        termino_norm = normalizar_texto(termino_busqueda)
        mascara = (
            (df_filtrado['Concepto'].apply(normalizar_texto) == termino_norm) |
            (df_filtrado['Sub unidad'].apply(normalizar_texto) == termino_norm) |
            (df_filtrado['Unidad'].apply(normalizar_texto) == termino_norm)
        )
        return df_filtrado[mascara][col_mes].sum()

    def sum_tipo_robusto(tipo_str):
        tipo_norm = normalizar_texto(tipo_str)
        mascara = (
            (df_filtrado['Descripción tipo'].apply(normalizar_texto) == tipo_norm) |
            (df_filtrado['Tipo'].apply(normalizar_texto) == tipo_norm)
        )
        return df_filtrado[mascara][col_mes].sum()

    # ---- KPI 1: INGRESO POR CUOTAS DE GRADO (positiva) ----
    ing_cuotas_grado = abs(sum_concepto_robusto('INGR. CUOTAS GRADO'))

    # Descuentos institucionales (valores absolutos positivos)
    bonificaciones = abs(sum_concepto_robusto('BONIFICACIONES'))
    reduc_becas = abs(sum_concepto_robusto('REDUCC. BECAS'))
    reduc_sede = abs(sum_concepto_robusto('REDUCC. SEDE'))

    # ---- KPI 2: INGRESOS NETOS ----
    ingresos_netos = ing_cuotas_grado - bonificaciones - reduc_becas - reduc_sede

    # Componentes intermedios de la escalera de ingresos
    ing_matriculas = abs(sum_concepto_robusto('INGR. MATRICULAS GRADO'))
    cursos_extension = abs(sum_concepto_robusto('CURSOS EXTENSION'))
    ingresos_varios = abs(sum_concepto_robusto('INGRESOS VARIOS'))
    ing_financieros = abs(sum_concepto_robusto('INGR. FINANCIEROS'))

    # Base total de ingresos consolidada
    total_ingresos_base = ingresos_netos + ing_matriculas + cursos_extension + ingresos_varios + ing_financieros

    # ---- KPI 3: EGRESOS TOTALES ----
    gastos_personal = abs(sum_tipo_robusto('GTOS PERSONAL'))
    gastos_funcionamiento = abs(sum_tipo_robusto('GTOS FUNCIONAM.'))
    egresos_totales = gastos_personal + gastos_funcionamiento

    # ---- KPI 4: INVERSIONES TOTALES (Estructura Corregida por Concepto) ----
    # 1. Inversiones en Obras Civiles
    const_edificios = abs(sum_concepto_robusto('Construcción de Edificios'))
    ampliacion_mejoras = abs(sum_concepto_robusto('Ampliac.y mejoras edificios'))
    inversiones_obra = const_edificios + ampliacion_mejoras
    
    # 2. Inversiones Operativas (Búsqueda por los 7 conceptos indicados)
    inv_bibliografia = abs(sum_concepto_robusto('Bibliografía'))
    inv_bibliotecas_dig = abs(sum_concepto_robusto('Bibliotecas Digitales'))
    inv_equipamiento = abs(sum_concepto_robusto('Equipamiento'))
    inv_audio_tv = abs(sum_concepto_robusto('Equipos audio y tv'))
    inv_informaticos = abs(sum_concepto_robusto('Equipos Informáticos'))
    inv_muebles = abs(sum_concepto_robusto('Muebles y Utiles e Instalaciones'))
    
    inversiones_operativas = (
        inv_bibliografia + inv_bibliotecas_dig + inv_equipamiento + 
        inv_audio_tv + inv_informaticos + inv_muebles
    )

    # Consolidado de Inversiones Totales
    inversiones_totales = inversiones_obra + inversiones_operativas

    # =========================================================
    # CÁLCULO DE LA ESCALERA DE RESULTADOS (RESTA MATEMÁTICA PURA)
    # =========================================================
    resultado_operativo_excl = (
        ingresos_netos + ing_matriculas + cursos_extension + ingresos_varios
    ) - gastos_personal - gastos_funcionamiento - inversiones_operativas

    resultado_operativo_incl = resultado_operativo_excl + ing_financieros
    resultado_final = resultado_operativo_incl - inversiones_obra

    # Margen porcentual oficial del Resultado Final
    margen_porcentual = (resultado_final / total_ingresos_base * 100) if total_ingresos_base > 0 else 0

    # =========================================================
    # CÁLCULO DE PORCENTAJES CON REDONDEO FLOTANTE PARA CONCEPCIÓN
    # =========================================================
    suma_flujos_barra = ingresos_netos + egresos_totales + inversiones_totales

    if suma_flujos_barra > 0:
        # Usamos round(..., 1) en vez de int() para que valores chicos como 0.7% no desaparezcan
        porcentaje_ingresos = round((ingresos_netos / suma_flujos_barra) * 100, 1)
        porcentaje_egresos = round((egresos_totales / suma_flujos_barra) * 100, 1)
        porcentaje_inversiones = round((inversiones_totales / suma_flujos_barra) * 100, 1)
    else:
        porcentaje_ingresos, porcentaje_egresos, porcentaje_inversiones = 33.3, 33.3, 33.4

    # Formateadores numéricos adaptados al esquema contable del Excel objetivo
    def fmt_positivo(valor):
        return f"$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def fmt_negativo(valor):
        # Formateamos el número y lo envolvemos en un span rojo
        num_formateado = f"-$ {abs(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f'<span style="color: #dc3545; font-weight: bold;">{num_formateado}</span>'

    # =========================================================
    # 3. INTERFAZ GRÁFICA DE KPIs ORIGINALES 
    # =========================================================
    st.markdown("### Indicadores generales")

    kpi1_html = crear_kpi_html("Cuotas Grado", fmt_positivo(ing_cuotas_grado), "border-margen")
    kpi2_html = crear_kpi_html("Ingresos Netos", fmt_positivo(ingresos_netos), "border-ingresos")
    kpi3_html = crear_kpi_html("Egresos Totales", fmt_negativo(egresos_totales), "border-egresos")
    kpi4_html = crear_kpi_html("Inversiones Totales", fmt_negativo(inversiones_totales), "border-inversiones")

    # Si el resultado es negativo usa el formateador rojo, si no, el positivo normal
    fmt_res = fmt_negativo(resultado_final) if resultado_final < 0 else fmt_positivo(resultado_final)
    kpi5_html = crear_kpi_html("Resultado Final", fmt_res, "border-resultado")#, f"{margen_porcentual:.1f} %")

    # Grid responsive: reacomoda las 5 tarjetas (5 -> 3 -> 2 -> 1 por fila)
    # en vez de forzar 5 columnas angostas de Streamlit. Mismos estilos,
    # solo cambia el contenedor.
    st.markdown(
        f'<div class="kpi-grid">{kpi1_html}{kpi2_html}{kpi3_html}{kpi4_html}{kpi5_html}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### Distribución del Presupuesto")
    
    # Mandamos los porcentajes con decimales flotantes al componente de la barra
    crear_barra(
        ingresos=porcentaje_ingresos,
        egresos=porcentaje_egresos,
        inversiones=porcentaje_inversiones
    )

    # Gráficos
    st.markdown("---")
    graf1, graf2 = st.columns(2)

    with graf1:
        st.info("Consolidado UNSTA")
        #abrir_card("📋 Consolidado UNSTA")
        
        # 1. Calculamos los márgenes intermedios de las 3 etapas como pide el PPT
        m_excl = (resultado_operativo_excl / total_ingresos_base * 100) if total_ingresos_base > 0 else 0
        m_incl = (resultado_operativo_incl / total_ingresos_base * 100) if total_ingresos_base > 0 else 0
        m_final = (resultado_final / total_ingresos_base * 100) if total_ingresos_base > 0 else 0

        # 2. Guardamos todo en la valija de datos
        paquete_datos = {
            'ing_cuotas_grado': ing_cuotas_grado,
            'bonificaciones': bonificaciones,
            'reduc_becas': reduc_becas,
            'reduc_sede': reduc_sede,
            'ingresos_netos': ingresos_netos,
            'ing_matriculas': ing_matriculas,
            'cursos_extension': cursos_extension,
            'ingresos_varios': ingresos_varios,
            'gastos_personal': gastos_personal,
            'gastos_funcionamiento': gastos_funcionamiento,
            'inversiones_operativas': inversiones_operativas,
            'resultado_operativo_excl': resultado_operativo_excl,
            'ing_financieros': ing_financieros,
            'resultado_operativo_incl': resultado_operativo_incl,
            'inversiones_obra': inversiones_obra,
            'resultado_final': resultado_final,
            'margen_excl': m_excl,
            'margen_incl': m_incl,
            'margen_final': m_final
        }
        
        # 3. Dibujamos la tabla idéntica al PPT dentro del card
        crear_tabla_consolidado(paquete_datos)
        
        cerrar_card()
        st.empty()

    with graf2:
        st.info("Mayores Conceptos Consolidados")
        # Cambiamos el nombre al que realmente tiene la función internamente
        crear_grafico_mayores_conceptos(paquete_datos)
        st.empty()
        
    crear_footer()