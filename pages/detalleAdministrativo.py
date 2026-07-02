import streamlit as st
import pandas as pd

def cargar_vista_administrativa(seleccion_filtro):
    """Maneja el bloque administrativo de manera totalmente desacoplada"""
    st.markdown(f"### 📋 Indicadores Generales: {seleccion_filtro}")
    
    # Simulación de KPIs fijos administrativos
    dkpi1, dkpi2 = st.columns(2)
    with dkpi1:
        st.markdown("""
            <div style="background:white; padding:15px; border-radius:12px; border-left:6px solid #005088; box-shadow:0px 2px 8px rgba(0,0,0,0.05);">
                <div style="font-size:14px; color:#64748b; font-weight:500;">Cantidad de Administrativos</div>
                <div style="font-size:24px; font-weight:bold; color:#1e293b; margin-top:5px;">420</div>
            </div>
        """, unsafe_allow_html=True)
    with dkpi2:
        st.markdown("""
            <div style="background:white; padding:15px; border-radius:12px; border-left:6px solid #cbd5e1; box-shadow:0px 2px 8px rgba(0,0,0,0.05);">
                <div style="font-size:14px; color:#64748b; font-weight:500;">$ Disponible Proyectado</div>
                <div style="font-size:24px; font-weight:bold; color:#1e293b; margin-top:5px;">$ 24.506 M</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("Módulo administrativo unificado y listo para cargar data de Excel.")