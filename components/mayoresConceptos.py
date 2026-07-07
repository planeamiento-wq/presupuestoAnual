import streamlit as st
import plotly.express as px
import pandas as pd

def crear_grafico_mayores_conceptos(datos_calculados):
    """
    Renderiza el gráfico de barras horizontales con los mayores conceptos consolidados.
    Usa la misma paleta de colores institucional del tablero.
    """
    c = datos_calculados

    # 1. Armamos la lista de conceptos con sus magnitudes absolutas para el ordenamiento
    # Estructuramos el tipo para mapear los colores institucionales
    lista_conceptos = [
        {"Concepto": "INGR. CUOTAS GRADO", "Monto": c['ing_cuotas_grado'], "Tipo": "Ingresos", "Valor_Real": c['ing_cuotas_grado']},
        {"Concepto": "BONIFICACIONES", "Monto": c['bonificaciones'], "Tipo": "Egresos", "Valor_Real": -c['bonificaciones']},
        {"Concepto": "REDUCC. BECAS", "Monto": c['reduc_becas'], "Tipo": "Egresos", "Valor_Real": -c['reduc_becas']},
        {"Concepto": "REDUCC. SEDE", "Monto": c['reduc_sede'], "Tipo": "Ingresos", "Valor_Real": -c['reduc_sede']}, # Descuentos de ingresos
        {"Concepto": "INGR. MATRICULAS DE GRADO", "Monto": c['ing_matriculas'], "Tipo": "Ingresos", "Valor_Real": c['ing_matriculas']},
        {"Concepto": "CURSOS EXTENSION", "Monto": c['cursos_extension'], "Tipo": "Ingresos", "Valor_Real": c['cursos_extension']},
        {"Concepto": "INGRESOS VARIOS", "Monto": c['ingresos_varios'], "Tipo": "Ingresos", "Valor_Real": c['ingresos_varios']},
        {"Concepto": "GASTOS EN PERSONAL", "Monto": c['gastos_personal'], "Tipo": "Egresos", "Valor_Real": -c['gastos_personal']},
        {"Concepto": "GASTOS DE FUNCIONAMIENTO", "Monto": c['gastos_funcionamiento'], "Tipo": "Egresos", "Valor_Real": -c['gastos_funcionamiento']},
        {"Concepto": "INVERSIONES OPERATIVAS", "Monto": c['inversiones_operativas'], "Tipo": "Inversiones", "Valor_Real": -c['inversiones_operativas']},
        {"Concepto": "INGR. FINANCIEROS", "Monto": c['ing_financieros'], "Tipo": "Ingresos", "Valor_Real": c['ing_financieros']},
        {"Concepto": "INVERSIONES OBRAS", "Monto": c['inversiones_obra'], "Tipo": "Inversiones", "Valor_Real": -c['inversiones_obra']}
    ]

    # Convertimos a DataFrame y ordenamos de mayor a menor según el tamaño de la barra (Monto absoluto)
    df_graf = pd.DataFrame(lista_conceptos)
    df_graf = df_graf.sort_values(by="Monto", ascending=True) # Ascending True porque Plotly grafica de abajo hacia arriba

    # Mapeo de colores idéntico a tu barra de progreso
    color_map = {
        "Ingresos": "#a2dbb1",    # Verde suave
        "Egresos": "#f4b6c6",     # Rosa / Rojo suave
        "Inversiones": "#fcd38a"  # Amarillo / Naranja suave
    }

    # Formateador de etiquetas para las barras (Formato contable argentino)
    df_graf['Texto_Etiqueta'] = df_graf['Valor_Real'].apply(
        lambda x: f"$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if x >= 0 
        else f"-$ {abs(x):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )

    # 2. Creamos el gráfico horizontal con Plotly
    fig = px.bar(
        df_graf,
        x="Monto",
        y="Concepto",
        color="Tipo",
        orientation="h",
        color_discrete_map=color_map,
        text="Texto_Etiqueta"
    )

    # 3. Afinamos el diseño estético para que quede limpio y profesional
    fig.update_layout(
        showlegend=True,
        legend_title_text="",
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        margin=dict(l=20, r=40, t=10, b=10),
        xaxis=dict(showgrid=False, visible=False), # Ocultamos el eje X para que no sature
        yaxis=dict(showgrid=False, title=""),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=420
    )

    fig.update_traces(
        textposition="outside", # Fuerza los números afuera de las barras
        textfont_size=11,
        cliponaxis=False
    )

    st.plotly_chart(fig, use_container_width=True)