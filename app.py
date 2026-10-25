# app.py
import streamlit as st
import json
from ai_service import fetch_ai_advice
from chart_builder import render_donut_chart

st.set_page_config(page_title="AI Financial Advisor", layout="wide")
st.title(" AI Financial Advisor & Budget Planner")

# Sidebar inputs for user financial profile
st.sidebar.header("Your Financial Profile")
salary = st.sidebar.number_input("Monthly Take-Home Salary", min_value=0, value=5000, step=100)
item_cost = st.sidebar.number_input("Target Item Cost", min_value=0, value=30000, step=500)
currency = st.sidebar.selectbox("Currency", ["CAD", "USD", "EUR", "GBP"])

# Main user query input
user_prompt = st.text_input("Ask your AI advisor a goal or question:", "Can I afford to buy this item on my salary?")

if st.button("Get AI Financial Advice"):
    if user_prompt:
        with st.spinner("Processing your request, depending on demand this may take up to ~30 seconds"):
            raw_response, used_model = fetch_ai_advice(salary, item_cost, currency, user_prompt)
            
            # Separate text response from JSON chart payload
            if "```json" in raw_response:
                parts = raw_response.split("```json")
                ai_text = parts[0].strip()
                json_part = parts[1].split("```")[0].strip()
                
                # Display text advice
                st.subheader("Advisor Insights")
                st.write(ai_text)
                
                # Parse JSON and render donut chart
                try:
                    data = json.loads(json_part)
                    render_donut_chart(data["categories"], data["values"], currency)
                except Exception as e:
                    st.error(f"Could not parse chart data: {e}")
            else:
                st.subheader("Advisor Insights")
                st.write(raw_response)
    else:
        st.warning("Please enter a question or goal.")