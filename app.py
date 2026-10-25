# app.py
import streamlit as st
import json
from ai_service import fetch_ai_advice

from chart_builder import render_donut_chart

st.set_page_config(page_title="AI Financial Advisor", layout="wide") #general ui config and title 
st.title(" AI Financial Advisor & Budget Planner")

#SLIDER SETTINGS AND CONFIG
# Sidebar inputs for user financial profile UI CHANGES  uses a button to use sliders or text input values 
st.sidebar.header("Your Financial Profile") 

input_mode = st.sidebar.radio("Select Input Mode", ["Slider", "Number Input"])

if input_mode == "Slider":
    salary = st.sidebar.slider("Monthly Take-Home Salary", min_value=0, max_value=20000, value=5000, step=100)
    item_cost = st.sidebar.slider("Target Item Cost", min_value=0, max_value=100000, value=30000, step=500)
else:
    salary = st.sidebar.number_input("Monthly Take-Home Salary", min_value=0, max_value=10000000, value=5000, step=100)
    item_cost = st.sidebar.number_input("Target Item Cost", min_value=0, max_value=10000000, value=30000, step=500)
#select box for the currency
currency = st.sidebar.selectbox("Currency", ["CAD", "USD", "EUR", "GBP"])

# Main user input ( textbar for input )
user_prompt = st.text_input("Ask your AI advisor a goal or question:", "Can I afford to buy this item on my salary?")
#confirm ai use button, old one had used to much 
if st.button("Get AI Financial Advice"):
    if user_prompt:
        with st.spinner("Processing your request, depending on demand this may take up to ~30 seconds"): #because of a spinner being moved you can tell if your app is frozen or not
            raw_response, used_model = fetch_ai_advice(salary, item_cost, currency, user_prompt)
            
            # Separate text response from JSON chart payload
            if "```json" in raw_response:
                parts = raw_response.split("```json") #splits the ai response into 2 parts, one is the raw text and one is the json, then you take the key parts of the json into var
                ai_text = parts[0].strip()
                json_part = parts[1].split("```")[0].strip()
                
                # Display text advice
                st.subheader("Advisor Insights") #writes the first part of the response
                st.write(ai_text)
                
                # converts the json and render donut/pie chart
                try:
                    data = json.loads(json_part)
                    render_donut_chart(data["categories"], data["values"], currency)
                except Exception as e:
                    st.error(f"Could not parse chart data: {e}") # doesnt make the chart if it broke, returns an error message 
            else:
                st.subheader("Advisor Insights")
                st.write(raw_response)
    else:
        st.warning("Please enter a question or goal.")