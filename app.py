import os#this is for cleaning terminal for debugging 
import streamlit as st#this is the web ui powered by streamlit 
from google import genai          #imports google gemini


os.system('clear')#cleans the py vscode consol for bugs



st.title("AI integrated financial guide app")#title
st.write("This is my first app")#small about me we will remove this at the end? TBD


#the .x determins the type of ui the app uses so .slider creates a slider with the specified domains.
Salary = st.slider("Your ideal salary for purchace or finances", min_value=30000, max_value=300000, value=75000, step=1)#slider for salary + slider domain
Item_cost = st.slider("Cost of item or purchase", min_value=10, max_value=150000, value=40000, step=1)#slider for item cost + slider domain
currency = st.selectbox("Select Currency:", ["CAD", "USD"]) # Create a clean dropdown menu for currency

st.write(f"Your Salary: **${Salary}**")#telling the user what the salary is 
st.write(f"Your Item cost: **${Item_cost}**")#telling the user what the item cost
st.write(f"Your Currency is being calculated in: **{currency}**")

#begin the gemini section of the app

user_prompt = st.text_input("Ask your AI advisor a goal or question:")#creates the text box for users to input for ai
if user_prompt:
  with st.spinner("AI is processing your request"):
    client = genai.Client()
#what we will send to the gemini or ai being used to do the research for us which is out prompt and fills out the users inputed prices ( ai do be very picky so we had to filter out so much stuff with this)

    full_prompt = f"""
      The user's current salary is ${Salary} {currency}.
      The user is looking for an item which has a cost of ${Item_cost} {currency} and wants to buy it with their salary.
      If the user's salary or item cost is not specified, research and respond with them.
      If the user does not specify details about their item (like a car's mileage or trim), research and reply with a recommendation.
      User's goal/question: {user_prompt}
      
      IMPORTANT FORMATTING RULES:
      1. Keep the AI response to a minimum, clear, and concise.
      2. Always put a clear space between numbers and currency codes (e.g., "$40,000 CAD", never "$40,000CAD").
      3. STRICT RULE: Do NOT use any markdown bolding (**) or italics (*) inside your sentences. Write everything in clean, normal plain text. You may use bullet points (-) for lists, but no asterisks for text styling.
      """

   
    response = client.models.generate_content(
      model="gemini-3.5-flash", contents=full_prompt # used 3.5 flash because 3.8 was in high usage + tells the ai to use the variable full_prompt as the content of the request
    )
    st.subheader("AI Financial Advice:")  #yap to make the ui nicer
    clean_output = response.text.replace("*", "").replace("_", "") #writes the output after we filtered out all the FREEKING ERRORS AI GIVES US ( bro this took like 20 minutes 
    st.write(clean_output)    #writes the output after we filtered out all the FREEKING ERRORS AI GIVES US ( bro this took so long )
