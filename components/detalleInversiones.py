import plotly.graph_objects as go
import streamlit as st

# Mismo azul institucional que usa detalleGastos.py para "Desglose: Gastos
# de Funcionamiento", pero declarado acá de forma INDEPENDIENTE a propósito
# (no se importa desde detalleGastos.py): este componente queda aislado,
# así que un cambio futuro en uno no puede romper el otro.
COLOR_BASE_INVERSIONES = "#1F4EAA"


def renderizar_seccion_detalle_inversiones(
    nombre_unidad, config_colores, labels_inv=None, valores_inv=None
):
    """Gráfico de barras horizontales con el desglose de Inversiones (por
    Concepto: Equipos Informáticos, Mobiliario, Bibliografía, etc.) de la
    unidad académica o área administrativa seleccionada.

    Mismo lenguaje visual que 'Desglose: Gastos de Funcionamiento' (barras
    horizontales, azul institucional, texto adentro/afuera automático según
    el espacio), para que se sienta parte del mismo informe -- pero el
    código en sí es independiente del de detalleGastos.py.
    """
    color_texto = config_colores.get("texto", "#005088")

    if not labels_inv or not valores_inv:
        st.info(
            f"No se registran inversiones para {nombre_unidad} en el período seleccionado."
        )
        return

    st.markdown("---")
    st.markdown(
        '<div style="margin-top: 10px; margin-bottom: 15px;">'
        '<h4 style="color: #005088; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">'
        f'• Inversiones: <span style="color: {color_texto}; font-weight: 800;">{nombre_unidad}</span>'
        '</h4></div>',
        unsafe_allow_html=True,
    )

    textos_montos = [f"$ {v:,.0f}".replace(",", ".") for v in valores_inv]
    colores_barras = [COLOR_BASE_INVERSIONES] * len(labels_inv)

    fig = go.Figure(
        go.Bar(
            x=valores_inv,
            y=labels_inv,
            orientation="h",
            text=textos_montos,
            textposition="auto",  # Plotly decide: afuera si no entra, adentro si hay espacio.
            insidetextanchor="end",
            insidetextfont=dict(size=12, color="#FFFFFF", weight="bold"),
            outsidetextfont=dict(size=12, color="#1e293b", weight="bold"),
            marker=dict(color=colores_barras, line=dict(width=0)),
            hovertemplate="<b>%{y}</b><br>Inversión: %{text}<extra></extra>",
        )
    )

    fig.update_layout(
        height=max(220, len(labels_inv) * 55),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, b=10, l=10, r=80),
        xaxis=dict(
            showgrid=True,
            gridcolor="#f1f5f9",
            title=None,
            range=[0, max(valores_inv) * 1.15] if valores_inv else None,
        ),
        yaxis=dict(autorange="reversed", tickfont=dict(size=11, color="#475569")),
    )

    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})