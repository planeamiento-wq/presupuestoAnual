import plotly.graph_objects as go
import streamlit as st


def generar_degrade_pastel_seguro(hex_base, cantidad=4):
    """Genera variaciones armónicas de degradé bajando el brillo/saturación del

    color pastel inyectado, garantizando consistencia cromática.
    """
    try:
        base = hex_base.lstrip("#")
        r = int(base[0:2], 16)
        g = int(base[2:4], 16)
        b = int(base[4:6], 16)

        degrade = []
        for i in range(cantidad):
            # Vamos aclarando sutil y progresivamente el pastel base
            factor = 1.0 + (i * 0.15)
            new_r = min(255, int(r * factor if factor > 1 else r))
            new_g = min(255, int(g * factor if factor > 1 else g))
            new_b = min(255, int(b * factor if factor > 1 else b))

            # Ajuste secundario para dar distinción entre porciones
            if i == 1:
                new_r = max(0, new_r - 15)
            if i == 2:
                new_g = max(0, new_g - 15)
            if i == 3:
                new_b = max(0, new_b - 15)

            degrade.append(
                f"#{min(255, new_r):02x}{min(255, new_g):02x}{min(255, new_b):02x}"
            )
        return degrade
    except Exception:
        return ["#CBD5E1", "#E2E8F0", "#F1F5F9", "#F8FAFC"][:cantidad]


def renderizar_seccion_detalle_gastos(nombre_unidad, config_colores):
    """Componente agnóstico definitivo. Respeta la identidad pastel única de la

    unidad seleccionada tanto en barras como en porciones circulares.
    """
    color_texto = config_colores.get("texto", "#005088")
    color_pastel_base = config_colores.get("chip_bg", "#C7E8F7")

    st.markdown("---")
    st.markdown(
        f"""
        <div style="margin-top: 10px; margin-bottom: 25px;">
            <h4 style="color: #005088; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">
                📋 Detalles de Gastos: <span style="color: {color_texto}; font-weight: 800;">{nombre_unidad}</span>
            </h4>
        </div>
    """,
        unsafe_allow_html=True,
    )

    g_col1, g_col2 = st.columns([1.1, 1.2])

    # Generamos la paleta de la torta partiendo ÚNICAMENTE del pastel de la tarjeta
    colores_pie_armonicos = generar_degrade_pastel_seguro(
        color_pastel_base, cantidad=4
    )

    # --- GRÁFICO 1: PERSONAL (CIRCULAR) ---
    with g_col1:
        st.markdown(
            "<p style='font-weight: 700; color: #475569; text-align: center;"
            " margin-bottom: 15px;'>Distribución: Gastos de Personal</p>",
            unsafe_allow_html=True,
        )

        labels_p = [
            "Docentes Ordinarios",
            "Docentes Interinos",
            "Autoridades",
            "Adscritos / No Doc.",
        ]
        valores_p = [45, 30, 15, 10]

        fig_pie = go.Figure(
            go.Pie(
                labels=labels_p,
                values=valores_p,
                hole=0.45,
                marker=dict(
                    colors=colores_pie_armonicos,
                    line=dict(color="#ffffff", width=2),
                ),
                textinfo="percent",
                textposition="inside",
                textfont=dict(size=13, weight="bold", color="#1e293b"),
                hoverinfo="label+percent",
            )
        )

        fig_pie.update_layout(
            height=340,
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.05,
                xanchor="center",
                x=0.5,
                font=dict(size=11, color="#475569"),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(
            fig_pie, width="stretch", config={"displayModeBar": False}
        )

    # --- GRÁFICO 2: FUNCIONAMIENTO (BARRAS CON MONTOS COMPLETOS) ---
    with g_col2:
        st.markdown(
            "<p style='font-weight: 700; color: #475569; text-align: center;"
            " margin-bottom: 15px;'>Desglose: Gastos de Funcionamiento</p>",
            unsafe_allow_html=True,
        )

        cat_f = [
            "Servicios Básicos",
            "Insumos Laboratorio",
            "Licencias / Software",
            "Mantenimiento",
            "Viáticos y Extensión",
        ]

        # Montos completos reales (en pesos)
        val_f = [520000, 380000, 290000, 150000, 90000]

        # Formateo de cada valor a pesos completos con punto de miles ($ 520.000)
        textos_montos_completos = [
            f"$ {v:,.0f}".replace(",", ".") for v in val_f
        ]

        # Clavamos el mismo pastel exacto para que el bloque de barras sea limpio y uniforme
        colores_barras = [color_pastel_base] * 5

        fig_bar = go.Figure(
            go.Bar(
                x=val_f,
                y=cat_f,
                orientation="h",
                text=textos_montos_completos,  # Muestra los montos completos
                textposition="outside",
                textfont=dict(size=11, weight="bold", color="#1e293b"),
                marker=dict(color=colores_barras, line=dict(width=0)),
                hovertemplate=(
                    "<b>%{y}</b><br>Gasto: %{text}<extra></extra>"
                ),
            )
        )

        fig_bar.update_layout(
            height=340,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=10, b=10, l=10, r=60),  # Margen derecho ampliado para dar espacio al número completo
            xaxis=dict(showgrid=True, gridcolor="#f1f5f9", title=None),
            yaxis=dict(
                autorange="reversed",
                tickfont=dict(size=11, color="#475569"),
            ),
        )
        st.plotly_chart(
            fig_bar, width="stretch", config={"displayModeBar": False}
        )