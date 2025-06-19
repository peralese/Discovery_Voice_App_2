import os
from dotenv import load_dotenv
import json
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Optional explicit API key check (redundant if client is configured through env var)
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OpenAI API key not found. Did you forget to set it in your .env file?")

def get_next_question(context, last_response):
    unanswered = [k for k, v in context.items() if v is None]
    answered = {k: v for k, v in context.items() if v is not None}

    if not unanswered:
        return None

    prompt = f"""
You are a cloud migration discovery assistant. Your job is to help extract structured information from a client.

Here is what we already know:
{json.dumps(answered, indent=2)}

The user's last response was:
"{last_response}"

Here are the missing fields we still need:
{json.dumps(unanswered, indent=2)}

Please generate one clear, professional question that will help elicit one of the remaining fields. Return only the question itself.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful discovery agent conducting cloud architecture interviews."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=100
    )

    return response.choices[0].message.content.strip()

