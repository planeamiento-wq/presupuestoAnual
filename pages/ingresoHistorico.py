import streamlit as st
import plotly.graph_objects as go
from components.header import crear_header
from components.footer import crear_footer

def mostrar_historico(seleccion_filtro="General UNSTA", sede="Todas las Sedes"):
    
    # 1. Header Institucional
    crear_header(titulo="HISTÓRICO DE INGRESANTES", subtitulo=f"Evolución Anual de Matrícula Nueva — {sede}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Selector exclusivo de Sede
    col_selector, _ = st.columns([1, 2])
    with col_selector:
        sede_activa = st.selectbox(
            "Filtrar por Sede:", 
            ["Todas las Sedes", "Sede Central", "Sede Concepción", "Sede Yerba Buena"],
            index=["Todas las Sedes", "Sede Central", "Sede Concepción", "Sede Yerba Buena"].index(sede) if sede in ["Todas las Sedes", "Sede Central", "Sede Concepción", "Sede Yerba Buena"] else 0
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # DEFINICIÓN DE LA PALETA PASTEL UNIFICADA
    # ---------------------------------------------------------
    color_pastel_2024 = "#CBD5E1"  # Gris pastel
    color_pastel_2025 = "#93C5FD"  # Celeste pastel
    color_pastel_2026 = "#60A5FA"  # Azul pastel (Año actual)

    # Valores numéricos puros para el gráfico (según sede)
    if sede_activa == "Todas las Sedes":
        valores_anuales = [1250, 1480, 1610]
        ingresantes = {"2024": "1.250", "2025": "1.480", "2026": "1.610"}
    elif sede_activa == "Sede Central":
        valores_anuales = [850, 990, 1080]
        ingresantes = {"2024": "850", "2025": "990", "2026": "1.080"}
    else:
        valores_anuales = [400, 490, 530]
        ingresantes = {"2024": "400", "2025": "490", "2026": "530"}

    # ---------------------------------------------------------
    # KPIs CON DETALLES EN BORDES PASTEL (Alineados a la derecha)
    # ---------------------------------------------------------
    col_empuje, col_2024, col_2025, col_2026 = st.columns([1.3, 0.9, 0.9, 0.9])
    
    with col_2024:
        st.markdown(f"""
            <div style="background: white; padding: 15px; border-radius: 12px; border-left: 6px solid {color_pastel_2024}; box-shadow: 0px 4px 12px rgba(0,0,0,0.03); text-align: left;">
                <div style="font-size: 11px; color: #64748b; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px;">Ingresantes 2024</div>
                <div style="font-size: 26px; font-weight: bold; color: #475569; margin-top: 5px;">{ingresantes['2024']}</div>
            </div>
        """, unsafe_allow_html=True)

    with col_2025:
        st.markdown(f"""
            <div style="background: white; padding: 15px; border-radius: 12px; border-left: 6px solid {color_pastel_2025}; box-shadow: 0px 4px 12px rgba(0,0,0,0.03); text-align: left;">
                <div style="font-size: 11px; color: #64748b; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px;">Ingresantes 2025</div>
                <div style="font-size: 26px; font-weight: bold; color: #475569; margin-top: 5px;">{ingresantes['2025']}</div>
            </div>
        """, unsafe_allow_html=True)

    with col_2026:
        st.markdown(f"""
            <div style="background: white; padding: 12px 15px; border-radius: 12px; border-left: 6px solid {color_pastel_2026}; box-shadow: 0px 4px 12px rgba(0,0,0,0.03); text-align: left;">
                <div style="font-size: 11px; color: #64748b; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px;">Ingresantes 2026</div>
                <div style="font-size: 26px; font-weight: bold; color: #005088; margin-top: 5px;">{ingresantes['2026']}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # GRÁFICO COMPARATIVO ANUAL (Una barra por año con su color)
    # ---------------------------------------------------------
    st.markdown(f"<p style='font-weight: 700; color: #334155; font-size: 16px; margin-bottom: 15px;'>Tendencia de Crecimiento Interanual de Matrícula</p>", unsafe_allow_html=True)
    
    años = ['Año 2024', 'Año 2025', 'Año 2026']
    
    fig_anual = go.Figure()
    
    fig_anual.add_trace(go.Bar(
        x=años,
        y=valores_anuales,
        marker_color=[color_pastel_2024, color_pastel_2025, color_pastel_2026],
        text=[f"{v} Alumnos" for v in valores_anuales],
        textposition='outside', 
        textfont=dict(size=12, weight="bold", color="#475569"),
        width=[0.3, 0.3, 0.3], 
        showlegend=False 
    ))

    fig_anual.update_layout(
        height=350,
        bargap=0.6, 
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=20, b=10, l=10, r=10),
        xaxis=dict(showgrid=False, tickfont=dict(size=12, color="#475569", weight="bold")),
        yaxis=dict(showgrid=True, gridcolor="#f1f5f9", tickfont=dict(color="#64748b"), title="Total Ingresantes")
    )
    
    st.plotly_chart(fig_anual, width='stretch', config={'displayModeBar': False})    # 3. Footer
    crear_footer()