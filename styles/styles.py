import streamlit as st

def cargar_estilo():

    st.markdown("""
    <style>

    .stApp{
        background:#FAFAFA;
    }

    .titulo-portada{
        text-align:center;
        color:#44546A;
        font-size:56px;
        font-weight:700;
    }

    .subtitulo-portada{
        text-align:center;
        color:#6B7280;
        font-size:30px;
    }

    .descripcion{
        text-align:center;
        color:#6B7280;
        font-size:22px;
    }
    .titulo-dashboard{
    color:#0B69B3;
    font-size:34px;
    font-weight:700;
    }

    .subtitulo-dashboard{
        color:#6B7280;
        font-size:18px;
    }

    .footer{
        text-align:center;
        color:#8A8F98;
        font-size:15px;
        line-height:1.5;
    }

    .footer strong{
        color:#44546A;
        font-weight:700;
    }

    .kpi-card{

    background:white;

    border-radius:18px;

    padding:22px;

    box-shadow:0px 2px 10px rgba(0,0,0,.08);

    margin-bottom:10px;

    min-height:120px;

    }

    .kpi-title{

        color:#7A7A7A;

        font-size:15px;

    }

    .kpi-value{

        font-size:clamp(15px, 2.3vw, 23px); 

        font-weight:700;

        color:#374151;

        margin-top:12px;

        overflow-wrap:anywhere;

    }

    .kpi-delta{

        color:#5A8F63;

        font-size:13px;

        margin-top:12px;

    }

    .border-ingresos{

    border-left:8px solid #B8E3C6;

    }

    .border-egresos{

        border-left:8px solid #F3C4D6;

    }

    .border-inversiones{

        border-left:8px solid #F9E7A3;

    }

    .border-resultado{

        border-left:8px solid #BFD8FF;

    }

    .border-margen{

        border-left:8px solid #D9D2F4;

    }
    
    .card-dashboard{

    background:white;

    border-radius:18px;

    padding:22px;

    margin-bottom:25px;

    box-shadow:0px 2px 10px rgba(0,0,0,.08);

    }

    /* ===== RESPONSIVE: Tablets (max 992px) ===== */
    @media (max-width: 992px){
        .titulo-portada{
            font-size:42px;
        }
        .subtitulo-portada{
            font-size:24px;
        }
        .descripcion{
            font-size:18px;
        }
        .titulo-dashboard{
            font-size:28px;
        }
    }

    /* ===== KPI GRID: contenedor responsive para las tarjetas .kpi-card =====
       Reemplaza a st.columns(5) para que las tarjetas se reacomoden solas
       (5 -> 3 -> 2 -> 1 por fila) en vez de angostarse todas a la vez.
       No cambia ningún estilo visual de .kpi-card, solo el contenedor. */
    .kpi-grid{
        display:grid;
        grid-template-columns:repeat(auto-fit, minmax(175px, 1fr));
        gap:14px;
    }
    .kpi-grid .kpi-card{
        min-width:0;
    }

    /* ===== RESPONSIVE: Mobile (max 640px) ===== */
    @media (max-width: 640px){
        .titulo-portada{
            font-size:30px;
            line-height:1.2;
        }
        .subtitulo-portada{
            font-size:18px;
        }
        .descripcion{
            font-size:15px;
        }
        .titulo-dashboard{
            font-size:22px;
        }
        .subtitulo-dashboard{
            font-size:15px;
        }
        .kpi-card, .card-dashboard{
            padding:14px;
            border-radius:14px;
        }
        .kpi-value{
            font-size:19px;
        }
        .kpi-title{
            font-size:13px;
        }
        .footer{
            font-size:13px;
        }
    }

    </style>
    """, unsafe_allow_html=True)