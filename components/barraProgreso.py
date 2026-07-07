import plotly.graph_objects as go
import streamlit as st


def crear_barra(ingresos, egresos, inversiones):

    fig = go.Figure()

    # Barra de Ingresos
    fig.add_trace(
        go.Bar(
            x=[ingresos],
            y=[""],
            orientation="h",
            marker_color="#B8E3C6",
            name="Ingresos",
            text=[f"{ingresos}%"],        
            textposition="inside",        
            texttemplate="%{text}",       
            insidetextanchor="middle"    
        )
    )

    # Barra de Egresos
    fig.add_trace(
        go.Bar(
            x=[egresos],
            y=[""],
            orientation="h",
            marker_color="#F3C4D6",
            name="Egresos",
            text=[f"{egresos}%"],
            textposition="inside",
            texttemplate="%{text}",
            insidetextanchor="middle"     
        )
    )

    # Barra de Inversiones
    fig.add_trace(
        go.Bar(
            x=[inversiones],
            y=[""],
            orientation="h",
            marker_color="#F9E7A3",
            name="Inversiones",
            text=[f"{inversiones}%"],
            textposition="inside",
            texttemplate="%{text}",
            insidetextanchor="middle"     
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
            y=-0.55,               
            x=0.5,
            xanchor="center"
        ),
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="#333333"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True, 
        config={
            "displayModeBar": False
        }
    )