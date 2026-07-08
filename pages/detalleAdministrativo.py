import streamlit as st
from components.detalleGastos import renderizar_seccion_detalle_gastos

def cargar_vista_administrativa(seleccion_filtro, sede="Todas las Sedes", mes="Anual (Ene-Dic)"):
    """Maneja el bloque administrativo con una paleta pastel corporativa integrada"""
    
    config_admin = {
        "texto": "#005088",      # Azul UNSTA para tipografía principal
        "chip_bg": "#B9E1F7"     # Azul pastel institucional hermoso (Alto contraste, cero gris oscuro)
    }
    
    st.markdown(f"""
        <h3 style="margin-bottom: 25px; font-weight: 600; color: #475569;">
            Indicadores de Gestión: 
            <span style="color: #005088; font-size: 30px; font-weight: 800; margin-left: 5px;">
                {seleccion_filtro}
            </span>
        </h3>
    """, unsafe_allow_html=True)

    # Indicadores superiores compactos de dos columnas
    _, _,dkpi1, dkpi2 = st.columns([1, 1, 1, 1])
    
    with dkpi1:
        st.markdown("""
            <div style="background: white; padding: 15px; border-radius: 12px; border-left: 6px solid #005088; box-shadow: 0px 2px 8px rgba(0,0,0,0.05);">
                <div style="font-size: 12px; color: #64748b; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px;">Cantidad de Administrativos</div>
                <div style="font-size: 24px; font-weight: bold; color: #1e293b; margin-top: 5px;">420</div>
            </div>
        """, unsafe_allow_html=True)
        
    with dkpi2:
        st.markdown("""
            <div style="background: white; padding: 15px; border-radius: 12px; border-left: 6px solid #b9e1f7; box-shadow: 0px 2px 8px rgba(0,0,0,0.05);">
                <div style="font-size: 12px; color: #64748b; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px;">$ Disponible Proyectado</div>
                <div style="font-size: 24px; font-weight: bold; color: #1e293b; margin-top: 5px;">$ 24.506 M</div>
            </div>
        """, unsafe_allow_html=True)
        
    if seleccion_filtro != "Todas las Áreas":
        renderizar_seccion_detalle_gastos(seleccion_filtro, config_admin)
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("Módulo administrativo unificado. Seleccione un Servicio o Área arriba para auditar las partidas de Personal y Funcionamiento.")