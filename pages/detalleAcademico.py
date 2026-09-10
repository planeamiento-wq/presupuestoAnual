import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from components.detalleGastos import renderizar_seccion_detalle_gastos
from data.metricasAcademicas import (
    obtener_alumnos_activos_por_facultad,
    obtener_colaboradores_por_area,
    obtener_metricas_docentes,
    obtener_presupuesto_por_facultad,
    obtener_detalle_gastos_UA,
)

PALETA_FACULTADES_BASE = {
    "Todas las Facultades": {
        "bg": "#ffffff",
        "border": "#005088",
        "texto": "#005088",
        "chip_bg": "#e2e8f0",
        "doc": "580",
        "hs": "4.580",
    },
    "Facultad de Economía y Administración": {
        "bg": "#ffffff",
        "border": "#C2EABA",
        "texto": "#24A652",
        "chip_bg": "#B8E3C6",
        "doc": "165",
        "hs": "1.450",
    },
    "Facultad de Ciencias Jurídicas": {
        "bg": "#ffffff",
        "border": "#FBC4C0",
        "texto": "#F21905",
        "chip_bg": "#F3C4D6",
        "doc": "120",
        "hs": "1.100",
    },
    "Facultad de Ingeniería": {
        "bg": "#ffffff",
        "border": "#FCE2CD",
        "texto": "#F9812A",
        "chip_bg": "#AEC6CF",
        "doc": "95",
        "hs": "980",
    },
    "Facultad de Humanidades": {
        "bg": "#ffffff",
        "border": "#FEF3C7",
        "texto": "#FFA100",
        "chip_bg": "#F9E7A3",
        "doc": "80",
        "hs": "750",
    },
    "Facultad de Ciencias de la Salud": {
        "bg": "#ffffff",
        "border": "#C7E8F7",
        "texto": "#41A9DF",
        "chip_bg": "#E8D7F1",
        "doc": "120",
        "hs": "1.300",
    },
    "CEOP": {
        "bg": "#ffffff",
        "border": "#F3C4D6",
        "texto": "#B8144F",
        "chip_bg": "#F8E1EB",
        "doc": "15",
        "hs": "120",
    },
    "Dpto. de Formación Humanística": {
        "bg": "#ffffff",
        "border": "#A3C2C6",
        "texto": "#04474D",
        "chip_bg": "#D6E4E6",
        "doc": "10",
        "hs": "80",
    },
}

PALETA_FACULTADES = PALETA_FACULTADES_BASE


def formatear_monto_completo(valor):
    try:
        val_float = float(valor)
        return (
            f"$ {val_float:,.0f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
    except Exception:
        return "$ 0"


def obtener_paleta_dinamica(sede="Todas las Sedes", mes="Anual (Ene-Dic)"):
    dict_alumnos, total_alumnos_real = obtener_alumnos_activos_por_facultad(
        sede
    )
    dict_colaboradores = obtener_colaboradores_por_area(sede)

    # Traemos las métricas reales del archivo .parquet
    dict_docentes, total_doc_str, total_hs_str = obtener_metricas_docentes(
        sede
    )

    try:
        dict_presupuesto = obtener_presupuesto_por_facultad(sede, mes=mes)
    except TypeError:
        dict_presupuesto = obtener_presupuesto_por_facultad(sede)

    paleta_dinamica = {}
    total_colaboradores = sum(dict_colaboradores.values())
    total_presupuesto = sum(dict_presupuesto.values())

    for fac, config in PALETA_FACULTADES_BASE.items():
        paleta_dinamica[fac] = config.copy()

        if fac == "Todas las Facultades":
            paleta_dinamica[fac]["alum"] = (
                f"{total_alumnos_real:,.0f}".replace(",", ".")
            )
            paleta_dinamica[fac]["adm"] = str(total_colaboradores)
            paleta_dinamica[fac]["disp"] = formatear_monto_completo(
                total_presupuesto
            )
            # Asignamos los totales globales reales
            paleta_dinamica[fac]["doc"] = total_doc_str
            paleta_dinamica[fac]["hs"] = total_hs_str
        else:
            val_alum = dict_alumnos.get(fac, 0)
            val_adm = dict_colaboradores.get(fac, 0)
            val_pres = dict_presupuesto.get(fac, 0)

            # Datos específicos para la tarjeta de cada facultad
            datos_doc_fac = dict_docentes.get(fac, {"doc": "0", "hs": "0"})

            paleta_dinamica[fac]["alum"] = f"{val_alum:,.0f}".replace(
                ",", "."
            )
            paleta_dinamica[fac]["adm"] = str(val_adm)
            paleta_dinamica[fac]["disp"] = formatear_monto_completo(val_pres)
            paleta_dinamica[fac]["doc"] = datos_doc_fac["doc"]
            paleta_dinamica[fac]["hs"] = datos_doc_fac["hs"]

    return paleta_dinamica


def renderizar_kpis_superiores(datos_unidad, color_borde, color_texto):
    def html_kpi(titulo, valor):
        return (
            f'<div style="background: white; padding: 15px; border-radius: 12px; '
            f'border-left: 6px solid {color_borde}; box-shadow: 0px 4px 10px rgba(0,0,0,0.04); min-width: 0;">'
            f'<div style="font-size: 11px; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">{titulo}</div>'
            f'<div style="font-size: clamp(14px, 2vw, 20px); font-weight: 800; color: {color_texto}; margin-top: 5px; overflow-wrap: anywhere; word-break: normal;">{valor}</div>'
            f'</div>'
        )

    tarjetas = "".join([
        html_kpi("$ Disponible", datos_unidad["disp"]),
        html_kpi("Alumnos activos", datos_unidad["alum"]),
        html_kpi("Cant. Docentes", datos_unidad["doc"]),
        html_kpi("Horas Docentes", datos_unidad["hs"]),
        html_kpi("Cant. Colaboradores", datos_unidad["adm"]),
    ])

    # CSS Grid auto-fit: reacomoda las tarjetas (5 -> 3 -> 2 -> 1 por fila)
    # en vez de forzar 5 columnas angostas que rompen el texto.
    # Todo en una sola línea: si el HTML tiene saltos de línea con
    # indentación, Markdown puede interpretarlo como bloque de código
    # y mostrar las etiquetas como texto plano en vez de renderizarlas.
    st.markdown(
        f'<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 14px;">{tarjetas}</div>',
        unsafe_allow_html=True,
    )


def renderizar_bloques_facultades(paleta_actual):
    """Genera columnas dinámicas aumentando tamaño de fuente y ocultando las facultades sin actividad en la sede."""

    nombres_visibles = {
        "Facultad de Economía y Administración": "Economía y Adm.",
        "Facultad de Ciencias Jurídicas": "Ciencias Jurídicas",
        "Facultad de Ingeniería": "Ingeniería",
        "Facultad de Humanidades": "Humanidades",
        "Facultad de Ciencias de la Salud": "Ciencias de la Salud",
        "CEOP": "CEOP",
        "Dpto. de Formación Humanística": "Dpto. Form. Humanística",
    }

    facultades_activas = []
    for fac, config in PALETA_FACULTADES_BASE.items():
        if fac == "Todas las Facultades":
            continue

        datos = paleta_actual.get(fac, {})
        monto_str = datos.get("disp", "$ 0")
        alumnos_str = datos.get("alum", "0")

        monto_valido = monto_str != "$ 0" and monto_str != "$ 0,00"
        alumnos_validos = alumnos_str != "0"

        if monto_valido or alumnos_validos:
            facultades_activas.append((fac, datos, config))

    if not facultades_activas:
        st.info(
            "No hay unidades académicas registradas para la sede seleccionada."
        )
        return

    def html_bloque(titulo, datos, config):
        return (
            f'<div style="background: white; padding: 14px 10px; border-radius: 12px; '
            f'border-top: 5px solid {config["border"]}; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); min-height: 165px; min-width: 0;">'
            f'<div style="font-size: 15px; font-weight: 800; color: {config["texto"]}; text-align: center; margin-bottom: 8px; height: 38px; display: flex; align-items: center; justify-content: center; line-height: 1.15;">{titulo}</div>'
            f'<hr style="border: 0; border-top: 1px solid #f1f5f9; margin: 6px 0;">'
            f'<div style="margin-top: 6px;">'
            f'<span style="font-size: 10px; color: #64748b; font-weight: 800; letter-spacing: 0.5px;">DISPONIBLE:</span><br>'
            f'<span style="font-size: clamp(12px, 1.6vw, 14px); font-weight: 800; color: #1e293b; overflow-wrap: anywhere;">{datos["disp"]}</span>'
            f'</div>'
            f'<div style="margin-top: 10px; display: flex; justify-content: space-between; font-size: 13px; color: #475569; gap: 6px;">'
            f'<div style="min-width:0;">Alumn:<br><strong style="color:#1e293b; font-size: 14px;">{datos["alum"]}</strong></div>'
            f'<div style="text-align: right; min-width:0;">Doc:<br><strong style="color:#1e293b; font-size: 14px;">{datos["doc"]}</strong></div>'
            f'</div>'
            f'</div>'
        )

    bloques = "".join(
        html_bloque(nombres_visibles.get(fac, fac), datos, config)
        for fac, datos, config in facultades_activas
    )

    # CSS Grid auto-fit: reacomoda de N columnas a menos filas más anchas
    # a medida que se achica la pantalla, en vez de comprimir todas las
    # facultades en la misma fila fija. Todo en una sola línea (ver nota
    # arriba sobre el bug de Markdown con HTML indentado).
    st.markdown(
        f'<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 14px;">{bloques}</div>',
        unsafe_allow_html=True,
    )


def renderizar_grafico_participacion(sede="Todas las Sedes"):
    dict_presupuesto = obtener_presupuesto_por_facultad(sede)

    colores_map = {
        "Facultad de Ciencias de la Salud": "#C7E8F7",
        "Facultad de Economía y Administración": "#C2EABA",
        "Facultad de Ciencias Jurídicas": "#FBC4C0",
        "Facultad de Ingeniería": "#FCE2CD",
        "Facultad de Humanidades": "#FEF3C7",
        "CEOP": "#F3C4D6",
        "Dpto. de Formación Humanística": "#A3C2C6",
    }

    nombres_cortos = {
        "Facultad de Ciencias de la Salud": "Ciencias de la Salud",
        "Facultad de Economía y Administración": "Economía y Administración",
        "Facultad de Ciencias Jurídicas": "Ciencias Jurídicas",
        "Facultad de Ingeniería": "Ingeniería",
        "Facultad de Humanidades": "Humanidades",
        "CEOP": "CEOP",
        "Dpto. de Formación Humanística": "Dpto. Form. Humanística",
    }

    total = sum(dict_presupuesto.values())
    datos = []

    if total > 0:
        for fac, monto in dict_presupuesto.items():
            if monto > 0:
                pct = round((monto / total) * 100, 1)
                nombre = nombres_cortos.get(fac, fac)
                color = colores_map.get(fac, "#e2e8f0")
                datos.append((nombre, pct, color))

        datos.sort(key=lambda x: x[1], reverse=True)

    if not datos:
        return

    datos_plotly = list(reversed(datos))

    unidades = [d[0] for d in datos_plotly]
    porcentajes = [d[1] for d in datos_plotly]
    colores_pasteles = [d[2] for d in datos_plotly]
    textos_etiquetas = [f"{p:.1f}%" for p in porcentajes]

    fig = go.Figure(
        go.Bar(
            x=porcentajes,
            y=unidades,
            orientation="h",
            text=textos_etiquetas,
            textposition="outside",
            textfont=dict(size=13, color="#1e293b", family="Arial"),
            marker=dict(color=colores_pasteles, line=dict(width=0)),
            hovertemplate="<b>%{y}</b><br>Participación: %{x}%<extra></extra>",
        )
    )

    fig.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(r=50, t=20, b=30, l=10),
        height=max(200, len(unidades) * 45),
        xaxis=dict(range=[0, 35]),
        yaxis=dict(tickfont=dict(size=13, color="#475569")),
    )

    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


def cargar_vista_academica(
    seleccion_filtro, sede="Todas las Sedes", mes="Anual (Ene-Dic)"
):
    paleta_dinamica = obtener_paleta_dinamica(sede=sede, mes=mes)
    cfg = paleta_dinamica.get(
        seleccion_filtro, PALETA_FACULTADES_BASE["Todas las Facultades"]
    )

    st.markdown(
        f"""
        <h3 style="margin-bottom: 25px; font-weight: 600; color: #005088;">
            Indicadores |   
            <span style="color: {cfg['texto']}; font-size: 30px; font-weight: 800; margin-left: 5px;">
                {seleccion_filtro}
            </span>
        </h3>
    """,
        unsafe_allow_html=True,
    )

    if seleccion_filtro != "Todas las Facultades":
        renderizar_kpis_superiores(cfg, cfg["border"], cfg["texto"])

        # 1. Obtenemos los datos calculados desde el Excel
        labels_p, val_p, cat_f, val_f = obtener_detalle_gastos_UA(
            seleccion_filtro, sede=sede, mes=mes
        )

        # 2. Inyectamos los datos reales al componente gráfico
        renderizar_seccion_detalle_gastos(
            seleccion_filtro,
            cfg,
            labels_p=labels_p,
            valores_p=val_p,
            cat_f=cat_f,
            val_f=val_f,
        )

        st.markdown("<br>", unsafe_allow_html=True)
    else:
        renderizar_kpis_superiores(cfg, "#005088", "#005088")
        st.markdown("<br>", unsafe_allow_html=True)

        renderizar_bloques_facultades(paleta_dinamica)

        # NOTAS ACLARATORIAS (ahora arriba del título de distribución,
        # en vez de al pie). HTML en una sola línea para que Markdown
        # lo renderice bien.
        st.markdown(
            '<div style="margin-top: 25px; padding-top: 12px; '
            'display: flex; gap: 30px; justify-content: flex-end; align-items: center;">'
            '<p style="font-size: 11px; color: #64748b; margin: 0;">'
            '<strong style="color: #005088; text-transform: uppercase; font-size: 10px; letter-spacing: 0.4px;">• Total de Docentes:</strong> '
            'Contabiliza docentes únicos. La suma por unidad puede ser mayor por múltiples cargos.'
            '</p>'
            '<p style="font-size: 11px; color: #64748b; margin: 0;">'
            '<strong style="color: #005088; text-transform: uppercase; font-size: 10px; letter-spacing: 0.4px;">• Datos y Presupuesto:</strong> '
            'Sincronizado con bases locales. Consolida rubros estrictamente académicos.'
            '</p>'
            '</div>',
            unsafe_allow_html=True,
        )

        # TÍTULO DEL GRÁFICO
        st.markdown(
            '<div style="margin-top: 25px; margin-bottom: 15px;">'
            '<strong style="color: #005088; font-size: 15px; text-transform: uppercase; letter-spacing: 0.5px;">'
            'Distribución Porcentual del Presupuesto Asignado'
            '</strong>'
            '</div>',
            unsafe_allow_html=True,
        )

        # GRÁFICO DE BARRAS
        renderizar_grafico_participacion(sede=sede)