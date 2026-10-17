import os
import streamlit as st
from google import genai
from google.genai import errors

st.title("AI integrated financial guide app")
st.write("This is my first app")

# Sliders
Salary = st.slider("Your ideal salary for purchase or finances", min_value=30000, max_value=300000, value=75000, step=1)
Item_cost = st.slider("Cost of item or purchase", min_value=10, max_value=150000, value=40000, step=1)
currency = st.selectbox("Select Currency:", ["CAD", "USD"])

st.write(f"Your Salary: **${Salary:,}**")
st.write(f"Your Item cost: **${Item_cost:,}**")
st.write(f"Your Currency is being calculated in: **{currency}**")

user_prompt = st.text_input("Ask your AI advisor a goal or question:")

if user_prompt:
    with st.spinner("AI is processing your request"):
        client = genai.Client()

        full_prompt = f"""
        The user's current salary is ${Salary} {currency}.
        The user is looking for an item which has a cost of ${Item_cost} {currency} and wants to buy it with their salary.
        If the user's salary or item cost is not specified, research and respond with them.
        If the user does not specify details about their item (like a car's mileage or trim), research and reply with a recommendation.
        User's goal/question: {user_prompt}
        
        IMPORTANT FORMATTING RULES:
        1. Keep the AI response to a minimum, clear, and concise.
        2. Always put a clear space between numbers and currency codes (e.g., "$40,000 CAD", never "$40,000CAD").
        3. STRICT RULE: Do NOT use any markdown formatting like bolding (**), italics (*), or backticks (`) inside your sentences. Write everything in clean, normal plain text. You may use bullet points (-) for lists, but no formatting symbols.
        """

        response = None
        used_fallback = False

        try:
            # Primary Tier: Gemini 3.5-flash
            response = client.models.generate_content(
                model="gemini-3.5-flash", contents=full_prompt
            )
        except Exception:
            used_fallback = True
            try:
                # Secondary Fallback Tier: Gemini 1.5-flash
                response = client.models.generate_content(
                    model="gemini-1.5-flash", contents=full_prompt
                )
            except Exception:
                response = None

        # Render outputs completely at the end
        if response:
            if used_fallback:
                st.warning(" **System Notice:** Gemini 3.5-flash capacity threshold reached. Multi-tier architectural fallback triggered: Routed request to Gemini 1.5-flash.")
            else:
                st.success(" **System Notice:** Request processed successfully using primary tier infrastructure (Gemini 3.5-flash).")
                
            st.subheader("AI Financial Advice:")
            
            clean_output = response.text.replace("*", "").replace("_", "").replace("`", "").replace("```", "")
            st.write(clean_output)
        else:
            st.error(" Both primary and fallback service tiers are currently unavailable. Please try again shortly.")
