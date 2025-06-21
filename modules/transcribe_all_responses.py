import json
import os
from modules.transcribe import transcribe_file

INPUT_FILE = "interview_log.json"
OUTPUT_FILE = "interview_log_transcribed.json"

transcribed_entries = []

# Ensure the input file exists
if not os.path.exists(INPUT_FILE):
    print(f"❌ {INPUT_FILE} not found.")
    exit(1)

with open(INPUT_FILE, "r") as f:
    for line in f:
        entry = json.loads(line)

        # Skip if already has a response
        if entry.get("response", "").strip():
            transcribed_entries.append(entry)
            continue

        audio_path = entry.get("audio_file")
        if audio_path and os.path.exists(audio_path):
            print(f"🔊 Transcribing: {audio_path}")
            try:
                text = transcribe_file(audio_path)
                entry["response"] = text.strip()
            except Exception as e:
                print(f"⚠️ Failed to transcribe {audio_path}: {e}")
        else:
            print(f"⚠️ Missing audio file: {audio_path}")

        transcribed_entries.append(entry)

# Save updated log
with open(OUTPUT_FILE, "w") as out:
    for entry in transcribed_entries:
        json.dump(entry, out)
        out.write("\n")

print(f"\n✅ Transcription complete. Output saved to {OUTPUT_FILE}")
