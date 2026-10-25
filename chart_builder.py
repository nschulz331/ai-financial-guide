import plotly.express as px
import streamlit as st

def render_donut_chart(chart_labels, chart_values, currency):
    fig = px.pie(names=chart_labels, values=chart_values, title="Financial Breakdown", hole=0.3, template="plotly_dark")
    fig.update_traces(textposition="outside", texttemplate="%{label}<br>%{percent} ($%{value:,.0f} " + currency + ")")
    st.plotly_chart(fig, use_container_width=True)