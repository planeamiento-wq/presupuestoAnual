import streamlit as st


def crear_footer():

    st.markdown("<div style='height:70px'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="footer">

        <hr style="width:45%; margin:auto; margin-bottom:15px;">

        Universidad del Norte Santo Tomás de Aquino<br>

        <strong>Servicio de Planeamiento Económico Financiero</strong>

        </div>
        """,
        unsafe_allow_html=True
    )