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
    answered = {k: v for k, v in context.items() if v}
    unanswered = [k for k, v in context.items() if not v]

    if not unanswered:
        return None

    prompt = f"""
You are an AI interview assistant helping gather technical discovery information for a cloud migration project.

Your job is to extract answers for the following structured discovery fields, one at a time.

Here is what we already know (already answered fields):
{json.dumps(answered, indent=2)}

Here are the remaining fields we still need to gather:
{json.dumps(unanswered, indent=2)}

The user's last response was:
\"\"\"{last_response}\"\"\"

⚠️ Do not ask about topics that already have answers — even if the answer is vague.
✅ You may follow up to clarify the user's last answer, IF you believe it helps gather one of the remaining fields.
🎯 Otherwise, ask a clean new question to collect one of the remaining fields.

Only ask ONE question at a time. Keep it professional and specific.

Return ONLY the question text.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if needed
        messages=[
            {
                "role": "system",
                "content": "You are a helpful cloud architecture discovery assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=150
    )

    return response.choices[0].message.content.strip()
