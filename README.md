
#   AI-Powered Financial Lifestyle Simulator 

A full-stack, interactive web application built with Streamlit and the Google GenAI SDK that lets users simulate financial goals, evaluate purchase decisions, and get context-aware, real-time AI financial advice.

##  Features
* **Interactive UI:** Dynamic sliders for salary and item/purchase costs, paired with a multi-currency selector (CAD/USD).
* **AI-Powered Insights:** Integrates multiple Google `gemini-flash-lite` models to analyze complex user-input scenarios, calculate estimated monthly expenses (loans, insurance, housing), and suggest realistic alternatives.
* **Robust Output Sanitization:** Custom text-scrubbing logic to ensure clean Markdown parsing and a seamless user experience.
* Pie Charts with `JSON` created from `Google Gemini` returned data from user input or default data if unchecked
##  Tech Stack
* **Frontend/UI:** Streamlit
* **AI Integration:** Google GenAI SDK (`google-genai`)
* **Environment:** Python 3 GitHub Codespaces

## Setup / Live Demo
**[Try the Live Web App Here](https://ai-financial-guide-2wzmqtvdgyz62foyrqwfpc.streamlit.app/)**


##  Future Plans:
* Interactive LIVE sliders ( current ones are not live)  ( the current ones just update the AI, might add a confirm changes buttons to them or revert to previous settings?
    -New sliders would be changed by AI (prompted?) TBD
* AI will use a Vehicle data API like MarketCheck for up to 5 listings but will attempt to find 3 ( still
  researching this for this feature since the whole finding keys is new still
 - Website data will then find the listing, and the listing will be checked with Gemini to return both
    - The link to the listing
    - Only returns the listings that are clean titles / salvaged / ext... (which will be prompted by the user)
    
* New charts according to each listing, including:
   - Km/miles graphs on ideal values, i.e., 100k km is roughly 1/4 the way until this car is at end of life 
   - Recommended salary to afford the car and then recommended financing
   - A down payment calculator to be added to the returned data
   - Add prices to the current graphs below the percents?
   - Options to toggle the above options
     
* Live sliders that actively change when clicking a submit/ update data button
  - These sliders will also change the pie charts, which will be created based on the user-inputted sliders,
  - If the user-inputted data is not changed, it will automatically change or recommend changing the sliders
    when prompted by the ai/ to the user to change the data.

 
