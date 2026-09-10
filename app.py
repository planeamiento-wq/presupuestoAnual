import pandas as pd
import streamlit as st
from components.card import abrir_card, cerrar_card
from components.footer import crear_footer
from components.header import crear_header
from components.kpiCard import crear_kpi
from pages.detalle import mostrar_detalle
from pages.ingresoHistorico import mostrar_historico
from pages.Resumen import mostrar_resumen
from styles.styles import cargar_estilo

try:
    from Resumen import mostrar_resumen
except ImportError:
    # Por si acaso dentro de carpeta pages/
    from pages.Resumen import mostrar_resumen

# CONFIGURACIÓN DE PÁGINA GLOBALES
st.set_page_config(page_title="Presupuesto Institucional", layout="wide")

# Llamo al CSS global
cargar_estilo()

# ------------------------------------------------------------------
# OCULTAR NAVEGACIÓN AUTOMÁTICA DE STREAMLIT (Carpetas /pages)
# ------------------------------------------------------------------
st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)


# ==== MENÚ LATERAL (Sidebar) ====
with st.sidebar:
    st.markdown(
        "<h2 style='text-align:center; color:#005088; margin-top:20px;'>Menú Presupuesto</h2>",
        unsafe_allow_html=True,
    )

    # Selector de páginas
    opcion_menu = st.radio(
        "Navegación:",
        [
            "Portada",
            "Resumen Ejecutivo",
            "Detalle Presupuestario",
            "Gráficos Históricos",
        ],
        label_visibility="collapsed",
    )

    # st.markdown("### Filtros Globales")
    # sede = st.selectbox("Sede:", ["Sede Central", "Sede Concepción", "Sede Yerba Buena"])
    # Smes_corte = st.select_slider("Mes de corte:", options=["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"], value="Jun")




# ==== LÓGICA DE NAVEGACIÓN ====

# Caso A: Si el usuario elige "Inicio / Portada", ejecutamos tu código original de portada
if opcion_menu == "Portada":
    
    # 1. CSS RESPONSIVO + FONDO OSCURO PROFUNDO (#033f5C)
    st.markdown("""
        <style>
        /* Cambiar el fondo de toda la aplicación a tu azul oscuro */
        .stApp {
            background-color: #033f5C !important;
        }
        
        /* Contenedor de las tarjetas de los bloques (Blancas y flotantes) */
        [data-testid="stMetric"] {
            background-color: #FFFFFF !important;
            padding: 1.8rem !important;
            border-radius: 12px !important;
            border-top: 6px solid #005088 !important; /* Pasamos la línea arriba para guiar la mirada */
            box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.3) !important; /* Sombra más profunda para fondo oscuro */
            width: 100% !important;
            box-sizing: border-box !important;
        }
        
        /* Tipografías dentro de las tarjetas */
        [data-testid="stMetricLabel"] {
            color: #005088 !important;
            font-weight: 700 !important;
            font-size: clamp(0.8rem, 1vw, 1.1rem) !important;
            letter-spacing: 0.5px;
        }
        
        [data-testid="stMetricValue"] {
            font-size: clamp(1.3rem, 1.8vw, 1.7rem) !important;
            color: #1A1A1A !important;
            font-weight: 600 !important;
            white-space: normal !important;
        }
        
        /* Ajuste para las descripciones debajo de las tarjetas (Blanco suave para legibilidad) */
        .descripcion-bloque {
            color: #E0E0E0; 
            font-size: clamp(0.85rem, 0.95vw, 1rem); 
            margin-top: 12px; 
            line-height: 1.45;
        }

        /* El footer (componente compartido con el resto de la app) fue
           pensado para fondo claro. Acá, sobre el azul oscuro de la
           Portada, quedaba casi invisible -> lo re-coloreamos SOLO en
           esta página (este <style> solo se inyecta en la rama Portada,
           no afecta al footer en el resto de las páginas). */
        .footer {
            color: #A0B2C6 !important;
        }
        .footer strong {
            color: #FFFFFF !important;
        }
        .footer hr {
            border-top: 1px solid rgba(255,255,255,0.2) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. LOGO INSTITUCIONAL + MEMBRETE (Textos pasados a Blanco/Celeste para fondo oscuro)
    col_logo, col_titulos = st.columns([1, 6], gap="small")
    
    with col_logo:
        # Asegurate de que el logo sea PNG transparente. Si es blanco o color, va a resaltar hermoso.
        st.image("assets/logo_unsta.png", width=110) 
        
    with col_titulos:
        st.markdown(
            "<p style='color: #A0B2C6; font-size: clamp(11px, 0.8vw, 13px); margin-bottom: 0px; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 500; padding-top: 5px;'> "
            "Universidad del Norte Santo Tomás de Aquino &bull; Servicio de Planeamiento Económico Financiero"
            "</p>", 
            unsafe_allow_html=True
        )

        st.markdown(
            "<h1 style='color: #FFFFFF; font-size: clamp(2rem, 3.5vw, 2.8rem); font-weight: 800; margin-top: 5px; margin-bottom: 0px; line-height: 1.1; letter-spacing: -0.5px;'>"
            "PRESUPUESTO INSTITUCIONAL"
            "</h1>", 
            unsafe_allow_html=True
        )

        st.markdown(
            "<h3 style='color: #CBD5E1; font-size: clamp(1.2rem, 1.8vw, 1.5rem); font-weight: 400; margin-top: 5px; margin-bottom: 0px;'> "
            "Consolidado Anual &bull; Periodo Proyectivo 2026"
            "</h3>", 
            unsafe_allow_html=True
        )

    # Línea divisoria superior adaptada a fondo oscuro
    st.markdown("<hr style='margin-top: 25px; margin-bottom: 25px; border-top: 1px solid rgba(255,255,255,0.15);'>", unsafe_allow_html=True)

    # 3. DESCRIPCIÓN DEL ALCANCE (Texto en gris muy claro/blanco para que se lea perfecto)
    st.markdown(
        "<div style='font-size: clamp(1rem, 1.2vw, 1.15rem); color: #E2E8F0; line-height: 1.6; max-width: 65rem; margin-bottom: 1.5rem;'>"
        "Este portal interactivo presenta la planificación financiera anual estructurada para la totalidad de la institución. "
        "Centraliza los flujos de las <b>tres sedes institucionales</b>, desglosando el comportamiento de las unidades "
        "académicas y áreas administrativas, junto con un análisis analítico del comportamiento histórico de ingresantes."
        "</div>", 
        unsafe_allow_html=True
    )

    # 🛠️ BAJAR LAS TARJETAS: Agregamos un espacio vertical controlado antes de las columnas
    st.markdown("<br><br>", unsafe_allow_html=True)

    # 4. ÍNDICE DE MÓDULOS (Tarjetas blancas que contrastan con el fondo azul oscuro)
    # Reemplaza a st.metric (pensado para valores con variación -> de ahí el
    # badge verde con flecha, que no correspondía semánticamente acá).
    # HTML en una sola línea por tarjeta (evita que Markdown lo trate como
    # bloque de código) + CSS Grid auto-fit (mismo patrón responsive que
    # usamos en el resto de la app).
    # Íconos SVG en línea (estilo outline, minimalista) en vez de emojis:
    # se ven idénticos en cualquier navegador/SO y quedan más profesionales.
    icono_tendencia = (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#005088" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>'
        '<polyline points="17 6 23 6 23 12"></polyline>'
        '</svg>'
    )
    icono_sedes = (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#005088" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="3" y="3" width="7" height="7"></rect>'
        '<rect x="14" y="3" width="7" height="7"></rect>'
        '<rect x="14" y="14" width="7" height="7"></rect>'
        '<rect x="3" y="14" width="7" height="7"></rect>'
        '</svg>'
    )
    icono_graficos = (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#005088" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<line x1="18" y1="20" x2="18" y2="10"></line>'
        '<line x1="12" y1="20" x2="12" y2="4"></line>'
        '<line x1="6" y1="20" x2="6" y2="14"></line>'
        '</svg>'
    )

    modulos = [
        (icono_tendencia, "Bloque I", "Resumen Ejecutivo", "Visión Global",
         "Consolidado macro del presupuesto anual de la universidad. Análisis rápido de ingresos, egresos y balances generales."),
        (icono_sedes, "Bloque II", "Detalle Por Sedes", "Académico y Admin.",
         "Apertura analítica para las 3 sedes. Evaluación del presupuesto asignado a facultades y departamentos operativos."),
        (icono_graficos, "Bloque III", "Gráficos Históricos", "Anexo: Ingresantes",
         "Estudio evolutivo y comparativo del flujo de alumnos ingresantes en determinados periodos de tiempo claves."),
    ]

    def tarjeta_modulo(icono_svg, bloque, titulo, etiqueta, descripcion):
        return (
            '<div style="background: #F4F7FA; border-radius: 14px; padding: 26px 24px; '
            'border-top: 3px solid rgba(0, 80, 136, 0.4); box-shadow: 0px 4px 14px rgba(0,0,0,0.10); '
            'min-width: 0; height: 100%; display: flex; flex-direction: column; box-sizing: border-box;">'
            '<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 14px;">'
            f'<div style="width: 36px; height: 36px; border-radius: 10px; background: #E3EDF5; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">{icono_svg}</div>'
            f'<div style="font-size: 12px; font-weight: 700; letter-spacing: 0.5px; color: #005088; text-transform: uppercase;">{bloque}</div>'
            '</div>'
            f'<div style="font-size: 21px; font-weight: 800; color: #1e293b; margin-bottom: 12px; line-height: 1.2;">{titulo}</div>'
            f'<span style="display: inline-block; align-self: flex-start; background: #E3EDF5; color: #005088; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 999px; text-transform: uppercase; letter-spacing: 0.3px;">{etiqueta}</span>'
            f'<p style="font-size: 13.5px; color: #64748b; line-height: 1.55; margin-top: 16px; margin-bottom: 0; flex-grow: 1;">{descripcion}</p>'
            '</div>'
        )

    tarjetas_modulos = "".join(
        tarjeta_modulo(icono_svg, bloque, titulo, etiqueta, descripcion)
        for icono_svg, bloque, titulo, etiqueta, descripcion in modulos
    )

    # minmax(220px, 280px) en vez de (260px, 1fr): antes cada tarjeta se
    # estiraba para llenar todo el ancho disponible; ahora tienen un tope
    # de ancho y quedan centradas como grupo. align-items:stretch (+ height:100%
    # y flex en cada tarjeta) asegura que las 3 queden con la misma altura,
    # aunque las descripciones tengan distinto largo.
    st.markdown(
        f'<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 280px)); gap: 24px; justify-content: center; align-items: stretch;">{tarjetas_modulos}</div>',
        unsafe_allow_html=True,
    )

    # 5. ESPACIADO FINAL (antes tenía 4 <br> seguidos + el spacer propio del
    # footer -> dejaba un vacío enorme. Un solo spacer controlado alcanza).
    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

    # Tu componente original de Footer
    crear_footer()


# Caso B: Si elige "Resumen Ejecutivo", abrimos la "caja" de tu componente
elif opcion_menu == "Resumen Ejecutivo":
    mostrar_resumen()

# Caso C: Espacio reservado para lo que hagamos después
elif opcion_menu == "Detalle Presupuestario":
    mostrar_detalle()

# Caso D: Espacio reservado para los gráficos interanuales
elif opcion_menu == "Gráficos Históricos":
    mostrar_historico()