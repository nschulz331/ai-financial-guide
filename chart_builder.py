import plotly.express as px
import streamlit as st

def render_donut_chart(chart_labels, chart_values, currency):
    """
    Programmatically renders a clean monthly budget breakdown list 
    followed by the interactive Plotly donut chart.
    """
    
    # 1. Programmatically guarantee the text breakdown list always renders
    st.markdown("### Monthly Budget Breakdown")
    for label, val in zip(chart_labels, chart_values):
        st.markdown(f"- **{label}**: {val:,.2f} {currency}")

    st.divider()

    # 2. Render the interactive Plotly donut chart
    fig = px.pie(
        names=chart_labels, 
        values=chart_values, 
        title="Financial Breakdown", 
        hole=0.3, 
        template="plotly_dark"
    )
    
    fig.update_traces(
        textposition="outside", 
        texttemplate="%{label}<br>%{percent} ($%{value:,.0f} " + currency + ")"
    )
    
    st.plotly_chart(fig, use_container_width=True)