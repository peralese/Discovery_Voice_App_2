from unittest import result
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import tempfile

# Load environment variables and initialize OpenAI
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create the Flask app
app = Flask(__name__)

# Route to serve the main UI
@app.route("/")
def index():
    return render_template("index.html")

# Route to return a question (placeholder for now)
@app.route("/ask", methods=["POST"])
def ask_question():
    last_response = request.json.get("last_response", "")
    # You could integrate GPT logic here
    return jsonify({"question": "What is your name?"})

# Route to transcribe uploaded audio with Whisper
@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio uploaded"}), 400

    audio_file = request.files["audio"]

    try:
        # Save the uploaded audio to a temporary .webm file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            audio_file.save(tmp.name)
            tmp_path = tmp.name

        # Whisper transcription
        with open(tmp_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="text"
            )

        os.unlink(tmp_path)
        return jsonify({"transcript": result})


    except Exception as e:
        print("❌ Whisper transcription failed:", str(e))
        return jsonify({"error": "Transcription failed", "details": str(e)}), 500

# Run the app when executed directly
if __name__ == "__main__":
    app.run(debug=True)
