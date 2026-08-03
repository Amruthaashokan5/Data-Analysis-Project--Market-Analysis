import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

api_key = os.getenv("OPENROUTER_API_KEY")

print("API Key Found:", api_key is not None)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

try:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b:free",
        messages=[
            {
                "role": "user",
                "content": "Say hello! My OpenRouter API is working."
            }
        ]
    )

    print("\n===== AI Response =====\n")
    print(response.choices[0].message.content)

except Exception as e:
    print("\nError:")
    print(e)