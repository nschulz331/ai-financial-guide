
# AI-Powered Financial Lifestyle Simulator 

A full-stack, interactive web application built with Streamlit and the Google GenAI SDK that allows users to simulate financial goals, evaluate purchasing decisions, and receive context-aware, real-time AI financial advice.

##  Features
* **Interactive UI:** Dynamic sliders for salary and item/purchase costs, paired with a multi-currency selector (CAD/USD).
* **AI-Powered Insights:** Integrates Google's `gemini-3.5-flash` model to analyze complex financial scenarios, calculate estimated monthly expenses (loans, insurance, housing), and suggest realistic alternatives.
* **Robust Output Sanitization:** Custom text-scrubbing logic to ensure clean markdown parsing and a seamless user experience.

##  Tech Stack
* **Frontend/UI:** Streamlit
* **AI Integration:** Google GenAI SDK (`google-genai`)
* **Environment:** Python 3.14, GitHub Codespaces

##  Setup & Installation
1. Clone the repository:
   ```bash
git clone https://github.com/nschulz331/ai-financial-guide.git
cd ai-financial-guide
