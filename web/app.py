from flask import Flask, request, jsonify, send_from_directory, session, render_template
from werkzeug.utils import secure_filename
from openai import OpenAI
import os
import uuid
import tempfile
import json

# --- Flask setup ---
app = Flask(__name__)
app.secret_key = "your_super_secret_key"  # Required for session support

# --- OpenAI setup ---
client = OpenAI()

# --- Interview schema ---
discovery_schema = {
    "interviewee_name": None,
    "application_name": None,
    "architecture_overview": None,
    "business_processes": None,
    "user_concurrency": None,
    "databases": None,
    "technology_stack": None,
    "current_hosting": None,
    "security_compliance": None,
    "deployment_process": None,
    "sla_metrics": None,
    "backup_strategy": None,
    "known_issues": None
}

# --- Routes ---

@app.route("/")
def index():
    session["context"] = discovery_schema.copy()
    session["last_response"] = ""
    session["first_question_asked"] = False
    session["name_received"] = False
    return render_template("index.html")

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio = request.files["audio"]
    filename = secure_filename(f"{uuid.uuid4().hex}.webm")

    temp_path = os.path.join(tempfile.gettempdir(), filename)
    audio.save(temp_path)

    try:
        with open(temp_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text",
                language="en"
            )
        return jsonify({"transcript": transcript})
    except Exception as e:
        print("❌ Transcription failed:", str(e))
        return jsonify({"error": "Transcription failed", "details": str(e)}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.route("/ask", methods=["POST"])
def ask():
    try:
        if "context" not in session:
            session["context"] = discovery_schema.copy()
            session["last_response"] = ""
            session["first_question_asked"] = False
            session["name_received"] = False

        context = session["context"]
        last_response = request.json.get("last_response", "").strip()

        # STEP 1: Always ask name first
        if not session.get("first_question_asked"):
            if last_response:
                context["interviewee_name"] = last_response
                session["last_response"] = last_response
                session["name_received"] = True
                session["first_question_asked"] = True
            else:
                return jsonify({"question": "What is your name?"})

        # STEP 2: Store next unanswered response
        if session.get("first_question_asked") and last_response:
            for key in context:
                if context[key] is None:
                    context[key] = last_response
                    session["last_response"] = last_response
                    break

        # STEP 3: Generate next question
        answered = {k: v for k, v in context.items() if v}
        unanswered = [k for k, v in context.items() if not v]

        # if not unanswered:
        #     return jsonify({"done": True, "question": None})
        if not unanswered:
            return jsonify({
                "done": True,
                "question": None,
                "summary": context
            })


        prompt = f"""
You are an AI interview assistant helping gather technical discovery information for a cloud migration project.

Your job is to ask clear, professional questions — one at a time — to fill out this discovery schema.

Here is what we already know:
{json.dumps(answered, indent=2)}

Here are the remaining fields we still need to collect:
{json.dumps(unanswered, indent=2)}

The user's last response was:
\"\"\"{last_response}\"\"\"

⚠️ Do not repeat or rephrase questions for fields that already have values.
✅ Choose only ONE field from the remaining list and generate a targeted, professional question to help extract that value.

Return ONLY the question text.
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful discovery agent conducting cloud architecture interviews."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=100
        )

        question = response.choices[0].message.content.strip()
        return jsonify({"question": question})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# Serve JS files
@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    app.run(debug=True)

