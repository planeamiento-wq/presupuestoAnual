import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

PALETA_FACULTADES = {
    "Todas las Facultades": {
        "bg": "#ffffff", "border": "#005088", "texto": "#005088", "chip_bg": "#e2e8f0",
        "disp": "$ 24.906 M", "alum": "6.840", "doc": "580", "hs": "4.580", "adm": "95"
    },
    "Facultad de Economía y Administración": {
        "bg": "#ffffff", "border": "#C2EABA", "texto": "#24A652", "chip_bg": "#B8E3C6",
        "disp": "$ 7.160 M", "alum": "2.100", "doc": "165", "hs": "1.450", "adm": "28"
    },
    "Facultad de Ciencias Jurídicas": {
        "bg": "#ffffff", "border": "#FBC4C0", "texto": "#F21905", "chip_bg": "#F3C4D6",
        "disp": "$ 5.155 M", "alum": "1.450", "doc": "120", "hs": "1.100", "adm": "20"
    },
    "Facultad de Ingeniería": {
        "bg": "#ffffff", "border": "#FCE2CD", "texto": "#F9812A", "chip_bg": "#AEC6CF",
        "disp": "$ 3.437 M", "alum": "890", "doc": "95", "hs": "980", "adm": "15"
    },
    "Facultad de Humanidades": {
        "bg": "#ffffff", "border": "#FEF3C7", "texto": "#FFA100", "chip_bg": "#F9E7A3",
        "disp": "$ 2.864 M", "alum": "620", "doc": "80", "hs": "750", "adm": "12"
    },
    "Facultad de Ciencias de la Salud": {
        "bg": "#ffffff", "border": "#C7E8F7", "texto": "#41A9DF", "chip_bg": "#E8D7F1",
        "disp": "$ 6.290 M", "alum": "1.780", "doc": "120", "hs": "1.300", "adm": "20"
    }
}

def renderizar_kpis_superiores(datos_unidad, color_borde, color_texto):
    """Muestra la fila superior de 5 KPIs con bordes redondeados y colores dinámicos"""
    k_col1, k_col2, k_col3, k_col4, k_col5 = st.columns(5)
    
    def html_kpi(titulo, valor):
        return f"""
            <div style="background: white; padding: 15px; border-radius: 12px; border-left: 6px solid {color_borde}; box-shadow: 0px 4px 10px rgba(0,0,0,0.04);">
                <div style="font-size: 11px; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">{titulo}</div>
                <div style="font-size: 22px; font-weight: 800; color: {color_texto}; margin-top: 5px;">{valor}</div>
            </div>
        """
    
    with k_col1: st.markdown(html_kpi("$ Disponible", datos_unidad["disp"]), unsafe_allow_html=True)
    with k_col2: st.markdown(html_kpi("Cant. Alumnos", datos_unidad["alum"]), unsafe_allow_html=True)
    with k_col3: st.markdown(html_kpi("Cant. Docentes", datos_unidad["doc"]), unsafe_allow_html=True)
    with k_col4: st.markdown(html_kpi("Horas Docentes", datos_unidad["hs"]), unsafe_allow_html=True)
    with k_col5: st.markdown(html_kpi("Cant. Adm. Nodo", datos_unidad["adm"]), unsafe_allow_html=True)

def renderizar_bloques_facultades():
    """Muestra la cuadrícula general de las 5 facultades juntas (Vista Consolidada)"""
    b_col1, b_col2, b_col3, b_col4, b_col5 = st.columns(5)
    
    def html_bloque(titulo, datos, config):
        return f"""
            <div style="background: white; padding: 15px; border-radius: 14px; border-top: 6px solid {config['border']}; box-shadow: 0px 4px 12px rgba(0,0,0,0.06); min-height: 160px;">
                <div style="font-size: 18px; font-weight: bold; color: {config['texto']}; text-align: center; margin-bottom: 12px;">{titulo}</div>
                <hr style="border: 0; border-top: 1px solid #f1f5f9; margin: 8px 0;">
                <div style="margin-top: 6px;">
                    <span style="font-size: 10px; color: #64748b; font-weight: 600;">DISPONIBLE:</span><br>
                    <span style="font-size: 16px; font-weight: 800; color: #1e293b;">{datos['disp']}</span>
                </div>
                <div style="margin-top: 10px; display: flex; justify-content: space-between; font-size: 11px; color: #475569;">
                    <div>Alumnos:<br><strong style="color:#1e293b;">{datos['alum']}</strong></div>
                    <div style="text-align: right;">Docentes:<br><strong style="color:#1e293b;">{datos['doc']}</strong></div>
                </div>
            </div>
        """
        
    with b_col1: st.markdown(html_bloque("Economía y Adm.", PALETA_FACULTADES["Facultad de Economía y Administración"], PALETA_FACULTADES["Facultad de Economía y Administración"]), unsafe_allow_html=True)
    with b_col2: st.markdown(html_bloque("Ciencias Jurídicas", PALETA_FACULTADES["Facultad de Ciencias Jurídicas"], PALETA_FACULTADES["Facultad de Ciencias Jurídicas"]), unsafe_allow_html=True)
    with b_col3: st.markdown(html_bloque("Ingeniería", PALETA_FACULTADES["Facultad de Ingeniería"], PALETA_FACULTADES["Facultad de Ingeniería"]), unsafe_allow_html=True)
    with b_col4: st.markdown(html_bloque("Humanidades", PALETA_FACULTADES["Facultad de Humanidades"], PALETA_FACULTADES["Facultad de Humanidades"]), unsafe_allow_html=True)
    with b_col5: st.markdown(html_bloque("Ciencias de la Salud", PALETA_FACULTADES["Facultad de Ciencias de la Salud"], PALETA_FACULTADES["Facultad de Ciencias de la Salud"]), unsafe_allow_html=True)

def renderizar_grafico_participacion():
    """Genera un gráfico de barras horizontales puro e infalible con los colores clavados a mano"""
    
    # 1. Definimos los datos crudos en el orden EXACTO que querés que aparezcan de abajo hacia arriba
    # Sabiendo que Humanidades tiene el menor % (va abajo) y Economía el mayor (va arriba)
    unidades = [
        "Humanidades",
        "Ingeniería",
        "Ciencias Jurídicas",
        "Ciencias de la Salud",
        "Economía y Administración"
    ]
    
    porcentajes = [11.5, 13.8, 20.7, 25.3, 28.7]
    
    # 2. Inyectamos los colores pasteles de tus tarjetas en el orden EXACTO de la lista de arriba
    colores_pasteles = [
        "#FEF3C7",  # Humanidades (Amarillo pastel)
        "#FCE2CD",  # Ingeniería (Naranja pastel)
        "#FBC4C0",  # Ciencias Jurídicas (Coral/Rojo pastel)
        "#C7E8F7",  # Ciencias de la Salud (Celeste pastel)
        "#C2EABA"   # Economía y Adm. (Verde pastel)
    ]
    
    textos_etiquetas = [f"{p:.1f}%" for p in porcentajes]
    
    # 3. Construimos el gráfico con Graph Objects (Cero automatismos, control total)
    fig = go.Figure(go.Bar(
        x=porcentajes,
        y=unidades,
        orientation='h',
        text=textos_etiquetas,
        textposition='outside',
        textfont=dict(size=12, color="#1e293b"),
        marker=dict(
            color=colores_pasteles, # <-- Pintamos cada barra con su color correspondiente
            line=dict(width=0)       # Sin bordes feos
        ),
        hovertemplate="<b>%{y}</b><br>Participación: %{x}%<extra></extra>"
    ))
    
    # 4. Ajustes del contenedor estético
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=40, t=10, b=10),
        height=240,
        xaxis=dict(showgrid=True, gridcolor="#f1f5f9", range=[0, 40]),
        yaxis=dict(tickfont=dict(size=12, color="#475569"))
    )
    
    st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})

def cargar_vista_academica(seleccion_filtro, sede="Todas las Sedes", mes="Anual (Ene-Dic)"):
    """Orquesta exclusivamente el comportamiento del layout académico"""
    cfg = PALETA_FACULTADES[seleccion_filtro]
    
    st.markdown(f"""
        <h3 style="margin-bottom: 25px; font-weight: 600; color: #005088;">
            Indicadores Generales: 
            <span style="color: {cfg['texto']}; font-size: 30px; font-weight: 800; margin-left: 5px;">
                {seleccion_filtro}
            </span>
        </h3>
    """, unsafe_allow_html=True)
    
    if seleccion_filtro != "Todas las Facultades":
        renderizar_kpis_superiores(cfg, cfg["border"], cfg["texto"])
        st.markdown("<br>", unsafe_allow_html=True)
    else:
        renderizar_kpis_superiores(cfg, "#005088", "#005088")
        st.markdown("<br>", unsafe_allow_html=True)
        
        renderizar_bloques_facultades()
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
            <div style="margin-bottom: 10px;">
                <strong style="color: #005088; font-size: 15px; text-transform: uppercase; letter-spacing: 0.5px;">
                    📊 Distribución Porcentual del Presupuesto Asignado
                </strong>
            </div>
        """, unsafe_allow_html=True)
        
        renderizar_grafico_participacion()