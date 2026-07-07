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

        font-size:29px;

        font-weight:700;

        color:#374151;

        margin-top:12px;

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
    </style>
    """, unsafe_allow_html=True)