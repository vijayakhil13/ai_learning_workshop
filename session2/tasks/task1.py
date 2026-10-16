from groq import Groq

# 1. Initialize the client (picks up GROQ_API_KEY from environment)
client = Groq()

# 2. Make the API call
response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role": "user", "content": "Hello there!"}]
)

# 3. Print the result
print(response.choices[0].message.content)