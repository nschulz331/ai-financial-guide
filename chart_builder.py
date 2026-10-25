import plotly.express as px
import streamlit as st
#takes the json values and converts them into a pie chart with values and numbers and names with percents 
def render_donut_chart(chart_labels, chart_values, currency):
    fig = px.pie(names=chart_labels, values=chart_values, title="Financial Breakdown", hole=0.3, template="plotly_dark")
    fig.update_traces(textposition="outside", texttemplate="%{label}<br>%{percent} ($%{value:,.0f} " + currency + ")")
    st.plotly_chart(fig, use_container_width=True)