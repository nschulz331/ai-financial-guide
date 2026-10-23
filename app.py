import os  # this is for cleaning terminal for debugging
import streamlit as st  # this is the web ui powered by streamlit
from google import genai  # imports google gemini
from google.genai import errors

try:
    if "GEMINI_API_KEY" in st.secrets:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

use_user_data = False  # default value

st.title("AI integrated financial guide app")  # title
st.write("This is my first app")  # small about me

# asks the user if they would like to use the default data or custom data
use_user_data = st.checkbox(
    "I would like to use custom data (salary, price, currency) If left unchecked, the AI will use its own data to answer your questions",
    value=False,
)
if use_user_data == True:
    Salary = st.slider(
        "Your ideal salary for purchace or finances",
        min_value=30000,
        max_value=300000,
        value=75000,
        step=1,
    )  # slider for salary
    Item_cost = st.slider(
        "Cost of item or purchase", min_value=10, max_value=150000, value=40000, step=1
    )  # slider for item cost
    currency = st.selectbox(
        "Select Currency:", ["CAD", "USD"]
    )  # Create a clean dropdown menu for currency
else:
    st.write("Using default data for AI calculations")
    Salary = 75000
    Item_cost = 40000
    currency = "CAD"

# writes the info value bar
col1, col2, col3 = st.columns(3)
col1.metric("Salary", f"${Salary:,}")
col2.metric("Item Cost", f"${Item_cost:,}")
col3.metric("Currency", f"{currency}")


# begin the gemini section of the app
user_prompt = st.text_input("Ask your AI advisor a goal or question:")
if user_prompt:
    with st.spinner(
        "Processing your request, depending on demand this may take up to 30 seconds"
    ):
        client = genai.Client()

        # Cleaned up prompt instructions so the AI doesn't read python scripts inside it
        full_prompt = f"""
      The user's current salary is {Salary} {currency}.
      The user is looking for an item which has a cost of {Item_cost} {currency} and wants to buy it with their salary.
      If the user does not specify details about their item (like a car's mileage or trim), research and reply with a recommendation.
      User's goal/question: {user_prompt}
      
      CRITICAL INSTRUCTIONS:
      1. Keep the AI response clean, clear, and highly concise.
      2. DO NOT use backticks (`) or raw markdown code-blocks anywhere in your regular conversational paragraphs.
      3. Format financial values normally (e.g. 40,000 CAD or $40,000 CAD). Do not wrap them in spaces or quotes that look like variables.
      4. DO NOT write or mention model names (like Gemini 1.5 Pro) in the response text.

      At the very end of your response, output a JSON block wrapped in triple backticks exactly like this:
      ```json
      {{
        "categories": ["Recommended Salary", "Monthly Payment", "Monthly Savings", "Downpayment Required", "Leftover Monthly Income"],
        "values": [90000, 4500, 600, 5000, 3200]
      }}
      ```
      The values array must only contain numbers for plotting.
      """

        try:
            # 1st Choice: Highest free tier rate limits
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite", contents=full_prompt
            )
            used_model = "gemini-3.5-flash-lite"

        except Exception as e:
            error_msg = str(e).lower()
            if (
                "429" in error_msg
                or "resource_exhausted" in error_msg
                or "quota" in error_msg
            ):
                st.error(
                    "Free Tier Token Limit Reached! Please wait 60 seconds before trying again."
                )

            try:
                st.warning("Swapping to standard Flash backup model...")
                response = client.models.generate_content(
                    model="gemini-3.8-flash", contents=full_prompt
                )
                used_model = "gemini-3.8-flash"
            except Exception as e2:
                error_msg2 = str(e2).lower()
                if (
                    "429" in error_msg2
                    or "resource_exhausted" in error_msg2
                    or "quota" in error_msg2
                ):
                    st.error(
                        "Backup Model Quota Exhausted! Google Free Tier is temporarily locked."
                    )
                response = None
                used_model = "None"

        # Render the response and state the model used
        if response and response.text:
            # Displays your tracking badge
            st.info(f"Active Model: `{used_model}`")

            st.subheader("AI Financial Advice:")
            text_content = response.text

            # Splits JSON chart data from text description so it doesn't leak into the app view
            if "```json" in text_content:
                parts = text_content.split("```json")
                clean_output = parts[0]
                # Fixes squishing by rendering clean standard Markdown text blocks safely
                st.markdown(clean_output)
            else:
                st.markdown(text_content)
