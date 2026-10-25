from google import genai
import json

def fetch_ai_advice(salary, item_cost, currency, user_prompt):
    client = genai.Client()

    # Cleaned up prompt instructions so the AI doesn't read python scripts inside it
    full_prompt = f"""
    The user's current salary is {salary} {currency}.
    The user is looking for an item which has a cost of {item_cost} {currency}
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
        "categories": ["Rent & Housing", "Car/Item Monthly Payment", "Insurance & Fuel", "Food & Groceries", "Utilities & Bills", "Leftover Monthly Savings"],
        "values":
    }}
    ```
    The values array must only contain numbers for plotting. Ensure ALL numbers reflect a MONTHLY breakdown, and that all slices add up exactly to the user's total monthly take-home income.
    """

    try:
        # 1st Choice: Highest free tier rate limits
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite", contents=full_prompt
        )
        used_model = "gemini-3.5-flash-lite"
    except Exception:
            used_model = "None"
    return response.text, used_model