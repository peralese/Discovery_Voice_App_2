# Re-define the improved version of save_response after kernel reset
import json
from datetime import datetime

def save_response(question_id, response_text, audio_file=None):
    entry = {
        "question_id": question_id,
        "response": response_text,
        "timestamp": datetime.utcnow().isoformat()
    }

    if audio_file:
        entry["audio_file"] = audio_file

    # Load existing data if the file exists
    try:
        with open("interview_log.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    # Append new entry
    data.append(entry)

    # Write back to the file as a structured JSON list
    with open("interview_log.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Saved: {entry}")
