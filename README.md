
#   AI-Powered Financial Lifestyle Simulator 

A full-stack, interactive web application built with Streamlit and the Google GenAI SDK that allows users to simulate financial goals, evaluate purchasing decisions, and receive context-aware, real-time AI financial advice.

##  Features
* **Interactive UI:** Dynamic sliders for salary and item/purchase costs, paired with a multi-currency selector (CAD/USD).
* **AI-Powered Insights:** Integrates Google's `gemini-3.5-flash-lite` and `gemini-1.5-flash-lite` models to analyze complex user-input scenarios, calculate estimated monthly expenses (loans, insurance, housing), and suggest realistic alternatives.
* **Robust Output Sanitization:** Custom text-scrubbing logic to ensure clean Markdown parsing and a seamless user experience.

##  Tech Stack
* **Frontend/UI:** Streamlit
* **AI Integration:** Google GenAI SDK (`google-genai`)
* **Environment:** Python 3.14, GitHub Codespaces
##  Setup
1.

Clone your repository

Download your code into the new environment:

git clone https://github.com/nschulz331/ai-financial-guide.git

2. Move into the project folder

Change your terminal directory into the folder you just downloaded:

cd ai-financial-guide

3. Install the required dependencies

Install Streamlit and the Google GenAI library:

pip install streamlit google-genai

4. Set your Gemini API key

Pass your API key into the terminal session so the app can communicate with Google:

export GEMINI_API_KEY="your_actual_api_key_here"

5. Launch the app!

Fire up Streamlit:

streamlit run app.py

##
Codespaces will automatically pop up a notification saying your app is running on port 8503 and ask if you want to open it in your browser. Click Open in Browser, and you'll see your live application right away!
