from google import genai
import json

def fetch_ai_advice(salary, item_cost, currency, user_prompt, pre_tax, salary_mode):
    client = genai.Client()

    # Explicitly calculate and describe the salary so the AI doesn't confuse monthly/yearly
    if salary_mode == "Yearly":
        annual_val = salary * 12
        salary_text = f"{annual_val:,.2f} {currency} per year (which normalizes to {salary:,.2f} {currency} per month take-home)"
    else:
        annual_val = salary * 12
        salary_text = f"{salary:,.2f} {currency} per month (which equals {annual_val:,.2f} {currency} per year)"

    tax_status = "Before Tax (Pre-Tax)" if pre_tax else "After Tax (Post-Tax)"

    # Cleaned up prompt instructions with explicit monthly math bounds
    full_prompt = f"""
    The user's current salary is {salary_text}.
    The user's income tax status is: {tax_status}. however in your json you reply with at the end make sure to acount for the taxes in it so it doesnt plan for tax spending 
    if the taxes are before tax, if they are after tax then dont double up on the taxes 
    The user is looking for an item which has a cost of {item_cost} {currency} (note: this may be inaccurate to real market prices, so research and account for that in your response).
    If the user does not specify details about their item (like a car's mileage or trim), research and reply with a recommendation.
    User's goal/question: {user_prompt}
    
    complimentin the user at the beginning of your response is encouraged examples include statements like :
    "Congratulations on setting ambitious goals... a solid starting salary of 
    x per year. Your net monthly take-home pay will be approximately x  after taxes
    Regarding your ... purchase , x is a stunning choice. ( only include this if it is actualy dooable and also a good choice dont mislead them)
    acount for depreciation if specified at a specific age
    acount for the price of x if it is at a time in the fututre 


    CRITICAL INSTRUCTIONS:
    1. Keep the AI response clean, clear, and highly concise.
    2. DO NOT use backticks (`) or raw markdown code-blocks anywhere in your regular conversational paragraphs.
    3. Format financial values normally (e.g. 40,000 CAD or $40,000 CAD). Do not wrap them in spaces or quotes that look like variables.
    4. DO NOT write or mention model names (like Gemini) in the response text.
    5. DO NOT write out a bulleted or itemized monthly budget breakdown in your text response. Focus only on your advice and insights, as the 
    application will render the budget list automatically from your JSON data.
    
    At the very end of your response, output a JSON block wrapped in triple backticks exactly like this:
    ```json
    {{
        "categories": ["Rent & Housing", "Car/Item Monthly Payment", "Insurance & Fuel", "Food & Groceries", "Utilities & Bills", "Leftover Monthly Savings"],
        "values": [val1, val2, val3, val4, val5, val6]
    }}
    ```
    The values array must only contain numbers for plotting. Ensure ALL numbers reflect a MONTHLY breakdown, and that all slices add up exactly to the user's total monthly take-home income of {salary:,.2f} {currency}.
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite", contents=full_prompt
        )
        used_model = "gemini-3.5-flash-lite"
    except Exception as e:
        response = type('obj', (object,), {'text': f"Error generating content: {e}"})
        used_model = "None"
        
    return response.text, used_model