import streamlit as st
import plotly.express as px
import pandas as pd


def crear_grafico_consolidado():

    df = pd.DataFrame({

        "Concepto":[

            "Ingresos",
            "Egresos",
            "Inversiones"

        ],

        "Monto":[

            1250,
            980,
            180

        ]

    })

    fig = px.bar(

        df,

        x="Concepto",

        y="Monto",

        color="Concepto",

        color_discrete_map={

            "Ingresos":"#B8E3C6",

            "Egresos":"#F3C4D6",

            "Inversiones":"#F9E7A3"

        }

    )

    fig.update_layout(

        height=350,

        showlegend=False,

        paper_bgcolor="white",

        plot_bgcolor="white"

    )

    st.plotly_chart(

        fig,

        width="stretch",

        config={"displayModeBar":False}

    )