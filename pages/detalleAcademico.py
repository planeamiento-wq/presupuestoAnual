import streamlit as st

PALETA_FACULTADES = {
    "Todas las Facultades": {
        "bg": "#ffffff", "border": "#005088", "texto": "#005088", "chip_bg": "#e2e8f0",
        "disp": "$ 24.906 M", "alum": "6.840", "doc": "580", "hs": "4.580", "adm": "95"
    },
    "Facultad de Economía y Administración": {
        "bg": "#ffffff", "border": "#24A652", "texto": "#24A652", "chip_bg": "#B8E3C6",
        "disp": "$ 7.160 M", "alum": "2.100", "doc": "165", "hs": "1.450", "adm": "28"
    },
    "Facultad de Ciencias Jurídicas": {
        "bg": "#ffffff", "border": "#F21905", "texto": "#F21905", "chip_bg": "#F3C4D6",
        "disp": "$ 5.155 M", "alum": "1.450", "doc": "120", "hs": "1.100", "adm": "20"
    },
    "Facultad de Ingeniería": {
        "bg": "#ffffff", "border": "#F9812A", "texto": "#F9812A", "chip_bg": "#AEC6CF",
        "disp": "$ 3.437 M", "alum": "890", "doc": "95", "hs": "980", "adm": "15"
    },
    "Facultad de Humanidades": {
        "bg": "#ffffff", "border": "#FFA100", "texto": "#FFA100", "chip_bg": "#F9E7A3",
        "disp": "$ 2.864 M", "alum": "620", "doc": "80", "hs": "750", "adm": "12"
    },
    "Facultad de Ciencias de la Salud": {
        "bg": "#ffffff", "border": "#41A9DF", "texto": "#41A9DF", "chip_bg": "#E8D7F1",
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

def cargar_vista_academica(seleccion_filtro):
    """Orquesta exclusivamente el comportamiento del layout académico"""
    cfg = PALETA_FACULTADES[seleccion_filtro]
    
    # TÍTULO LIMPIO: Le quitamos el background y el padding al span del nombre
    st.markdown(f"""
        <h3 style="margin-bottom: 25px; font-weight: 600; color: #005088;">
            🎓 Indicadores Generales: 
            <span style="color: {cfg['texto']}; font-size: 30px; font-weight: 800; margin-left: 5px;">
                {seleccion_filtro}
            </span>
        </h3>
    """, unsafe_allow_html=True)
    
    # Renderizado condicional según filtro seleccionado
    if seleccion_filtro != "Todas las Facultades":
        renderizar_kpis_superiores(cfg, cfg["border"], cfg["texto"])
        st.markdown("<br>", unsafe_allow_html=True)
        # Acá podés agregar a futuro sub-filtros o tablas por unidad académica
    else:
        renderizar_kpis_superiores(cfg, "#005088", "#005088") # Totales en azul original
        st.markdown("<br>", unsafe_allow_html=True)
        renderizar_bloques_facultades()