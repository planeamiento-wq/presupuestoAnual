import streamlit as st

from styles.styles import cargar_estilo
from components.header import crear_header
from components.footer import crear_footer
from components.kpiCard import crear_kpi
from components.barraProgreso import crear_barra
from components.card import abrir_card, cerrar_card
from components.graficoConsolidado import crear_grafico_consolidado

def mostrar_resumen():
    #Llamo los componentes y estilo
    cargar_estilo()

    crear_header(
        "RESUMEN EJECUTIVO",
        "Seguimiento del presupuesto institucional"
    )

    # ==== KPIs ====
    st.markdown("### Indicadores generales")

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

    with kpi1:
        crear_kpi("Ingresos", "$ 1.250 M", "border-ingresos", "↑ +8%") # Asegurate de tener 'border-ingresos' en tu CSS

    with kpi2:
        crear_kpi("Egresos", "$ 980 M", "border-egresos", "↑ +5%")

    with kpi3:
        crear_kpi("Inversiones", "$ 180 M", "border-inversiones")

    with kpi4:
        crear_kpi("Resultado", "$ 90 M", "border-resultado")

    with kpi5:
        crear_kpi("Margen", "7,2 %", "border-margen")


    st.markdown("### Distribución del presupuesto")

    crear_barra(
        ingresos = 52,
        egresos = 36,
        inversiones = 12
    )


    # Gráficos

    st.markdown("---")

    graf1, graf2 = st.columns(2)

    with graf1:

        abrir_card("📋 Consolidado Presupuestario")

        crear_grafico_consolidado()

        cerrar_card()

        st.empty()

    with graf2:

        st.info("📊 Composición del Presupuesto")

        st.empty()


    st.markdown("---")

    st.info("📈 Evolución Mensual")

    st.empty()
    crear_footer()