import streamlit as st
import plotly.graph_objects as go
from components.header import crear_header 
from components.footer import crear_footer
from data.ingresantes import obtener_resumen_ingresantes_historico

def mostrar_historico():
    
    # 1. Header Institucional
    crear_header(titulo="HISTÓRICO DE INGRESANTES", subtitulo="Evolución Anual de Matrícula Nueva — Todas las Sedes")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. Obtener datos de MySQL (Vistas 2025 y 2026)
    df_raw = obtener_resumen_ingresantes_historico()

    # 3. Selector de Sede
    if not df_raw.empty and 'sede' in df_raw.columns:
        # Obtenemos valores únicos de la columna 'sede' y agregamos la opción global
        sedes_unicas = sorted([str(s) for s in df_raw['sede'].dropna().unique()])
        lista_sedes = ["Todas las Sedes"] + sedes_unicas
    else:
        # Respaldo si no hay datos o la BD aún no cargó
        lista_sedes = ["Todas las Sedes"]

    # Selector de Sede Dinámico
    col_selector, _ = st.columns([1.3, 2.7])
    with col_selector:
        sede_activa = st.selectbox("Filtrar por Sede:", lista_sedes, index = 0)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. VALOR DE 2024 HARCODEADO (provisorio hasta gestionar la vista)
    valores_2024_manual = {
        "Todas las Sedes": 1250,
        "CENTRAL": 850,
        "CONCEPCION": 200,
        "BUENOS AIRES": 200
    }
    val_2024 = valores_2024_manual.get(sede_activa, 1250)

    # 5. VALORES DE 2025 Y 2026 DESDE LA BASE DE DATOS
    val_2025 = 0
    val_2026 = 0

    if not df_raw.empty:
        if sede_activa != "Todas las Sedes":
            df_filtrado = df_raw[df_raw['sede'] == sede_activa]
        else:
            df_filtrado = df_raw

        totales = df_filtrado.groupby('anio')['total'].sum().to_dict()
        val_2025 = totales.get(2025, 0)
        val_2026 = totales.get(2026, 0)

    # Formateo con puntos para miles
    ingresantes_kpi = {
        "2024": f"{val_2024:,}".replace(",", "."),
        "2025": f"{val_2025:,}".replace(",", "."),
        "2026": f"{val_2026:,}".replace(",", ".")
    }

    # 6. PALETA DE COLORES PASTEL
    color_p_2024 = "#CBD5E1"  # Gris
    color_p_2025 = "#93C5FD"  # Celeste
    color_p_2026 = "#60A5FA"  # Azul

    # 7. TARJETAS KPI
    col_empuje, col_2024, col_2025, col_2026 = st.columns([1.1, 1, 1, 1])
    
    with col_2024:
        st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 12px; border-left: 6px solid {color_p_2024}; box-shadow: 0px 4px 12px rgba(0,0,0,0.03);">
                <div style="font-size: 11px; color: #64748b; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px;">INGRESANTES 2024</div>
                <div style="font-size: 32px; font-weight: bold; color: #1e293b; margin-top: 5px;">{ingresantes_kpi['2024']}</div>
            </div>
        """, unsafe_allow_html=True)

    with col_2025:
        st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 12px; border-left: 6px solid {color_p_2025}; box-shadow: 0px 4px 12px rgba(0,0,0,0.03);">
                <div style="font-size: 11px; color: #64748b; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px;">INGRESANTES 2025</div>
                <div style="font-size: 32px; font-weight: bold; color: #1e293b; margin-top: 5px;">{ingresantes_kpi['2025']}</div>
            </div>
        """, unsafe_allow_html=True)

    with col_2026:
        st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 12px; border-left: 6px solid {color_p_2026}; box-shadow: 0px 4px 12px rgba(0,0,0,0.03);">
                <div style="font-size: 11px; color: #64748b; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px;">INGRESANTES 2026</div>
                <div style="font-size: 32px; font-weight: bold; color: #1e293b; margin-top: 5px;">{ingresantes_kpi['2026']}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # 8. GRÁFICO DE BARRAS
    st.markdown("<p style='font-weight: 700; color: #1e293b; font-size: 17px; margin-bottom: 20px;'>Tendencia de Crecimiento Interanual de Matrícula</p>", unsafe_allow_html=True)
    
    años = ['Año 2024', 'Año 2025', 'Año 2026']
    valores_grafico = [val_2024, val_2025, val_2026]
    
    fig_anual = go.Figure()
    
    fig_anual.add_trace(go.Bar(
        x=años,
        y=valores_grafico,
        marker_color=[color_p_2024, color_p_2025, color_p_2026],
        text=[f"{v:,} Alumnos".replace(",", ".") if v > 0 else "" for v in valores_grafico],
        textposition='outside', 
        textfont=dict(size=12, weight="bold", color="#475569"),
        width=[0.35, 0.35, 0.35], 
        showlegend=False 
    ))

    fig_anual.update_layout(
        height=400,
        bargap=0.5, 
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=30, b=10, l=10, r=10),
        font=dict(family="Inter, sans-serif"),
        xaxis=dict(showgrid=False, tickfont=dict(size=13, color="#64748b", weight="bold")),
        yaxis=dict(
            showgrid=True, 
            gridcolor="#e2e8f0", 
            gridwidth=0.5,
            tickfont=dict(color="#64748b"), 
            title=dict(text="Total Ingresantes", font=dict(size=13, color="#64748b"))
        )
    )
    
    st.plotly_chart(fig_anual, use_container_width=True, config={'displayModeBar': False})
    
    # 9. Footer
    crear_footer()

if __name__ == "__main__":
    mostrar_historico()