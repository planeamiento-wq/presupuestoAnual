import streamlit as st


def crear_header(titulo, subtitulo):

    col1, col2 = st.columns([9, 2])

    with col1:

        st.markdown(
            f"""
            <div class="titulo-dashboard">
                {titulo}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="subtitulo-dashboard">
                {subtitulo}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.image("assets/logo2.png", width=250)

    st.markdown("""
    <hr style="
    border:none;
    height:3px;
    background:#0B69B3;
    margin-top:8px;
    margin-bottom:25px;
    ">
    """, unsafe_allow_html=True)