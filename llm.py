from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = os.getenv("MODEL_NAME")


def generate_reply(email):

    prompt = f"""
You are a professional customer support assistant answer politely don't to lengthy information.

Customer Email

Subject:
{email.subject}

Body:
{email.body}

Write a professional response.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content