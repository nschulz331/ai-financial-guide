import os#this is for cleaning terminal for debugging 
import streamlit as st#this is the web ui powered by streamlit 
from google import genai          #imports google gemini
from google.genai import errors
try:
    if "GEMINI_API_KEY" in st.secrets:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass


use_user_data = False #default value

st.title("AI integrated financial guide app")#title
st.write("This is my first app")#small about me we will remove this at the end? TBD
#asks the user if they would like to use the default data or custom data for the following variables.
use_user_data = st.checkbox("I would like to use custom data (salary, price, currency) If left unchecked, the AI will use its own data to answer your questions", value=False)#checkbox for askign to use custom data also the value = valse makes it so the box is unchecked by defauly
if use_user_data==True:
    Salary = st.slider("Your ideal salary for purchace or finances", min_value=30000, max_value=300000, value=75000, step=1)#slider for salary + slider domain
    Item_cost = st.slider("Cost of item or purchase", min_value=10, max_value=150000, value=40000, step=1)#slider for item cost + slider domain
    currency = st.selectbox("Select Currency:", ["CAD", "USD"]) # Create a clean dropdown menu for currency
else:
    st.write("Using default data for AI calculations") #if unchecked the app will use these base values 
    Salary = 75000
    Item_cost = 40000
    currency = "CAD"   

#writes the info value bar for the following variables
col1, col2, col3 = st.columns(3)
col1.metric("Salary", f"${Salary:,}")
col2.metric("Item Cost", f"${Item_cost:,}")
col3.metric("Currency", f"{currency}",)


#begin the gemini section of the app

user_prompt = st.text_input("Ask your AI advisor a goal or question:")
if user_prompt:
  with st.spinner("Processing your request, depending on demand this may take up to 30 seconds"):
    client = genai.Client()

    full_prompt = f"""
      The user's current salary is ${Salary} {currency}.
      The user is looking for an item which has a cost of ${Item_cost} {currency} and wants to buy it with their salary.
      If the user's salary or item cost is not specified, research and respond with them.
      If the user does not specify details about their item (like a car's mileage or trim), research and reply with a recommendation.
      User's goal/question: {user_prompt}
      
      IMPORTANT FORMATTING RULES:
      1. Keep the AI response to a minimum, clear, and concise.
      when writing things make sure to use the right spaces im using the streamlit and the this is my code for it:     if response:
      st.subheader("AI Financial Advice:")
      clean_output = response.text.replace("*", "").replace("_", "")
      st.write(clean_output) 
      i need you to like basicaly format it so it doesnt do random shit and like squish things together so format it apropriately avoid having
        the green boxes show up when writing Recommended Option: Buy a base new Mini Cooper (starts around 34,000 CAD) or a certified pre-owned 
        2021-2023 Mini Cooper (under 45,000 km) for 24,000 to 30,000 CAD. This brings your monthly payment to a safe range of 500 to $650 CAD. for example
      on the response because the numbers are showing up as variable boxes 

      also at the beginnign or end of each message you reply with you MUST state what gemini model you used
      """

    response = None

    try:
      # Try 3.8-flash first
      response = client.models.generate_content(
          model="gemini-3.8-flash", contents=full_prompt
      )
    except Exception:
      try:
        st.warning(
                  "Ai is limited right now due to high demand, swaping to backup models!"
              )
        # If 3.8 is busy, fall back to 3.5-flash
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite", contents=full_prompt
        )
        
      except Exception:
        # If both fail, response stays None
        response = None

    # Write the output ONCE down here IF we got a response
    if response:
      st.subheader("AI Financial Advice:")
      clean_output = response.text.replace("*", "").replace("_", "")
      st.write(clean_output)
    else:
      # Otherwise, show the warning box which is if the free api key is being limited by pro accounts. 
      st.warning(
          " All Google Gemini Ai models are currently in high use right now, please try again later,"
      )
