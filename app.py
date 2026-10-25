# app.py
import streamlit as st
import json
from ai_service import fetch_ai_advice
from chart_builder import render_donut_chart
from side_bar_ui import render_side_bar
salary, item_cost, currency, pre_tax, salary_mode = render_side_bar()
st.set_page_config(page_title="AI Financial Advisor", layout="wide") #general ui config and title 
st.title(" AI Financial Advisor & Budget Planner")




# Main user input ( textbar for input )
user_prompt = st.text_input("Ask your AI advisor a goal or question:", "Can I afford to buy this item on my salary?")
#confirm ai use button, old one had used to much 
if st.button("Get AI Financial Advice"):
    if user_prompt:
        with st.spinner("Processing your request, depending on demand this may take up to ~30 seconds"): #because of a spinner being moved you can tell if your app is frozen or not
            raw_response, used_model = fetch_ai_advice(salary, item_cost, currency, user_prompt, pre_tax, salary_mode)
            
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