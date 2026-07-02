import plotly.graph_objects as go
import streamlit as st


def crear_barra(ingresos, egresos, inversiones):

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=[ingresos],
            y=[""],
            orientation="h",
            marker_color="#B8E3C6",
            name="Ingresos",
        )
    )

    fig.add_trace(
        go.Bar(
            x=[egresos],
            y=[""],
            orientation="h",
            marker_color="#F3C4D6",
            name="Egresos",
        )
    )

    fig.add_trace(
        go.Bar(
            x=[inversiones],
            y=[""],
            orientation="h",
            marker_color="#F9E7A3",
            name="Inversiones",
        )
    )

    fig.update_layout(

        barmode="stack",

        height=90,

        margin=dict(
            l=20,
            r=20,
            t=10,
            b=35
        ),

        paper_bgcolor="#FAFAFA",

        plot_bgcolor="white",

        xaxis=dict(
            visible=False,
            range=[0,100]
        ),

        yaxis=dict(
            visible=False
        ),

        legend=dict(

            orientation="h",

            y=-0.45,

            x=0.5,

            xanchor="center"

        )

    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={
            "displayModeBar": False
        }
    )