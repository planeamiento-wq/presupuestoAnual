import streamlit as st


def abrir_card(titulo):

    st.markdown(
        f"""
        <div style="
            background:white;
            border-radius:18px;
            padding:20px;
            box-shadow:0px 2px 10px rgba(0,0,0,.08);
            margin-bottom:20px;
        ">
            <h4 style="
                margin-top:0;
                color:#44546A;
            ">
                {titulo}
            </h4>
        """,
        unsafe_allow_html=True
    )


def cerrar_card():

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )