import os
from dotenv import load_dotenv
from groq import Groq
from openai import OpenAI

load_dotenv()

# Test Groq
print("Testing Groq...")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
groq_response = groq_client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Say hello in one sentence."}]
)
print("Groq response:", groq_response.choices[0].message.content)

# Test OpenRouter
print("\nTesting OpenRouter...")
openrouter_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
openrouter_response = openrouter_client.chat.completions.create(
    model="openrouter/free",
    messages=[{"role": "user", "content": "Say hello in one sentence."}]
)

print("OpenRouter response:", openrouter_response.choices[0].message.content)
