import os
from groq import Groq


client = Groq()


# 1. SIMULATED DATABASE

def get_user_data(intent: str):
    if intent == "track_shipping":
        return {"order_id": "ORD-9921", "status": "Out for delivery via FedEx", "eta": "Today by 5 PM"}
    elif intent == "account_balance":
        return {"account_type": "Premium Pro", "balance": "$124.50", "renewal_date": "Nov 15, 2026"}
    return {}

# 2. INTENT DETECTION FUNCTION

def detect_intent(message: str) -> str:
    msg = message.lower()
    if "where" in msg or "package" in msg or "shipping" in msg:
        return "track_shipping"
    elif "balance" in msg or "money" in msg or "subscription" in msg:
        return "account_balance"
    return "general_help"


# 3. MAIN WORKFLOW TESTER

def test_context_workflow(user_message: str):
    print(f"\nUser Message: \"{user_message}\"")
    
    # Step 1: Detect Intent
    intent = detect_intent(user_message)
    print(f"Step 1 (Intent Detected): {intent}")

    # Step 2: Fetch Dynamic Context from Database
    context = get_user_data(intent)
    print(f"Step 2 (Context Fetched): {context}")

    # Step 3: Build Dynamic Prompt Template
    prompt = f"""
You are a helpful customer support assistant. Answer the user's question accurately using the live data context provided below.

[Live Data Context]
Intent: {intent}
Details: {context}

User Message: "{user_message}"
"""

    # Step 4: Send to LLM API
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You are a concise, accurate assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=256
    )

    print(f"Step 3 (AI Response):\n{response.choices[0].message.content}\n")

if __name__ == "__main__":

    test_context_workflow("can you tell me where my package is?")
    
    # Test account billing intent
    test_context_workflow("What is my current account balance and renewal date?")