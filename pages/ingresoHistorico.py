import pandas as pd
import plotly.express as px
import streamlit as st
from components.footer import crear_footer
from components.header import crear_header
from data.ingresantes import obtener_resumen_ingresantes_historico


def formatear_nombre_ua(nombre):
    """Inserta saltos de línea en nombres de facultades largos para mejorar la lectura en el eje X."""
    if not isinstance(nombre, str):
        return nombre

    reemplazos = {
        "Centro de Estudios de Filosofía y Teología de la Orden de Predicadores": (
            "CEOP"
        ),
        "DPTO de FORM. HUMAN-CRISTIANA": (
            "Dpto. Formación<br>Humanístico-Cristiana"
        ),
        "HUMANIDADES": (
            "Humanidades"
        ),
        "CS. JUR. POL. Y SOC.": "Ciencias Jurídicas,<br>Políticas y Sociales",
        "Ciencias Juridicas, Politicas y Sociales": (
            "Ciencias Jurídicas,<br>Políticas y Sociales"
        ),
        "Ciencias Jurídicas, Políticas y Sociales": (
            "Ciencias Jurídicas,<br>Políticas y Sociales"
        ),
        "ECONOMÍA Y ADMINISTRACIÓN": "Economía y<br>Administración",
        "INGENIERÍA": "Ingeniería",
        "CIENCIAS DE LA SALUD": "Ciencias de<br>la Salud",
        "FORMACION CONTINUA": "Formación<br>Continua",
        #"Formación Continua": "Formación<br>Continua",
    }
    return reemplazos.get(nombre, nombre)


def mostrar_historico():
    # 1. Header Institucional
    crear_header(
        titulo="HISTÓRICO DE INGRESANTES",
        subtitulo=(
            "Evolución Comparativa por Unidad Académica (Últimas 3 Cohortes) —"
            " UNSTA"
        ),
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Obtención de datos desde MySQL
    df_raw = obtener_resumen_ingresantes_historico()

    if df_raw.empty or "unidad" not in df_raw.columns:
        df_raw = pd.DataFrame(columns=["sede", "unidad", "anio", "total"])

    # 3. Selector por Sede
    sedes_unicas = (
        sorted([str(s) for s in df_raw["sede"].dropna().unique()])
        if not df_raw.empty
        else []
    )
    lista_sedes = ["Todas las Sedes"] + sedes_unicas

    col_selector, _ = st.columns([1.3, 2.7])
    with col_selector:
        sede_activa = st.selectbox("Filtrar por Sede:", lista_sedes, index=0)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Filtrado de datos por Sede
    if sede_activa != "Todas las Sedes" and not df_raw.empty:
        df_filtrado = df_raw[df_raw["sede"] == sede_activa].copy()
    else:
        df_filtrado = df_raw.copy()

    # Agrupar por Unidad Académica y Año
    if (
        not df_filtrado.empty
        and "unidad" in df_filtrado.columns
        and "anio" in df_filtrado.columns
    ):
        df_grafico = (
            df_filtrado.groupby(["unidad", "anio"])["total"].sum().reset_index()
        )
    else:
        df_grafico = pd.DataFrame(columns=["unidad", "anio", "total"])

    # Aseguramos formato texto para el año para el gráfico
    if not df_grafico.empty:
        df_grafico["anio"] = df_grafico["anio"].astype(str)
        df_grafico = df_grafico.sort_values(by=["unidad", "anio"])

    # 5. CÁLCULO Y SUMA REAL DE KPIS TOTALES
    totales_por_anio = (
        df_grafico.groupby("anio")["total"].sum().to_dict()
        if not df_grafico.empty
        else {}
    )

    # Detectar dinámicamente los 3 años presentes
    anios_presentes = sorted(list(totales_por_anio.keys()))
    anio_1 = anios_presentes[0] if len(anios_presentes) > 0 else "2024"
    anio_2 = anios_presentes[1] if len(anios_presentes) > 1 else "2025"
    anio_3 = anios_presentes[2] if len(anios_presentes) > 2 else "2026"

    val_anio_1 = totales_por_anio.get(anio_1, 0)
    val_anio_2 = totales_por_anio.get(anio_2, 0)
    val_anio_3 = totales_por_anio.get(anio_3, 0)

    # Formateo previo de cifras para evitar conflictos en el HTML
    kpi_1 = f"{val_anio_1:,.0f}".replace(",", ".")
    kpi_2 = f"{val_anio_2:,.0f}".replace(",", ".")
    kpi_3 = f"{val_anio_3:,.0f}".replace(",", ".")

    color_p_1, color_p_2, color_p_3 = "#CBD5E1", "#93C5FD", "#60A5FA"

    # TARJETAS KPI
    col_empuje, col_k1, col_k2, col_k3 = st.columns([1.1, 1, 1, 1])

    with col_k1:
        st.markdown(
            f"""
            <div style="background: white; padding: 10px; border-radius: 12px; border-left: 6px solid {color_p_1}; box-shadow: 0px 4px 12px rgba(0,0,0,0.03);">
                <div style="font-size: 11px; color: #64748b; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px;">INGRESANTES {anio_1}</div>
                <div style="font-size: 28px; font-weight: bold; color: #1e293b; margin-top: 5px;">{kpi_1}</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col_k2:
        st.markdown(
            f"""
            <div style="background: white; padding: 10px; border-radius: 12px; border-left: 6px solid {color_p_2}; box-shadow: 0px 4px 12px rgba(0,0,0,0.03);">
                <div style="font-size: 11px; color: #64748b; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px;">INGRESANTES {anio_2}</div>
                <div style="font-size: 28px; font-weight: bold; color: #1e293b; margin-top: 5px;">{kpi_2}</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col_k3:
        st.markdown(
            f"""
            <div style="background: white; padding: 10px; border-radius: 12px; border-left: 6px solid {color_p_3}; box-shadow: 0px 4px 12px rgba(0,0,0,0.03);">
                <div style="font-size: 11px; color: #64748b; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px;">INGRESANTES {anio_3}</div>
                <div style="font-size: 28px; font-weight: bold; color: #1e293b; margin-top: 5px;">{kpi_3}</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # 6. FORMATEAR NOMBRES PARA EL EJE X
    if not df_grafico.empty:
        df_grafico["ua_formatted"] = df_grafico["unidad"].apply(
            formatear_nombre_ua
        )
    else:
        df_grafico["ua_formatted"] = []

    # 7. GRÁFICO APILADO
    st.markdown(
        f"<p style='font-weight: 700; color: #1e293b; font-size: 17px;"
        f" margin-bottom: 20px;'>Volumen de Ingresantes por Unidad Académica"
        f" (Acumulado {anio_1} - {anio_3})</p>",
        unsafe_allow_html=True,
    )

    color_map = {anio_1: color_p_1, anio_2: color_p_2, anio_3: color_p_3}

    fig_stacked_ua = px.bar(
        df_grafico,
        x="ua_formatted",
        y="total",
        color="anio",
        #text="total",
        title="",
        color_discrete_map=color_map,
        labels={"ua_formatted": "", "total": "Alumnos", "anio": "Período"},
    )

    fig_stacked_ua.update_traces(
        textposition="inside",
        textfont=dict(size=11, color="#1e293b", family="Inter, sans-serif"),
        insidetextanchor="middle",
        hovertemplate=(
            "<b>%{x}</b><br>Año %{fullData.name}: %{y} alumnos<extra></extra>"
        ),
    )

    fig_stacked_ua.update_layout(
        height=470,
        barmode="stack",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, b=80, l=10, r=10),
        font=dict(family="Inter, sans-serif"),
        legend=dict(
            title="",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=11, color="#1e293b", weight="bold"),
            tickangle=0,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#e2e8f0",
            gridwidth=0.5,
            tickfont=dict(color="#64748b"),
            title=dict(
                text="Total Ingresantes",
                font=dict(size=12, color="#64748b"),
            ),
        ),
    )

    st.plotly_chart(
        fig_stacked_ua,
        use_container_width=True,
        config={"displayModeBar": False},
    )

    

    # 8. Footer
    crear_footer()


if __name__ == "__main__":
    mostrar_historico()