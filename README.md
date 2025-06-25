
# 🎙️ Voice Interview Bot – Dynamic Q&A Proof of Concept

This project is a proof of concept (PoC) for a **voice-enabled AI interview assistant** designed to gather cloud discovery information from users through dynamic conversation. It uses speech recognition, Whisper transcription, GPT-powered question generation, and structured context management.

---

## 🔧 Features

- Ask interview questions via **text-to-speech (TTS)** using `pyttsx3`
- Capture answers using **microphone input** via browser or terminal
- **Transcribe voice responses using OpenAI Whisper API**
- Store both **audio (.wav/.webm)** and **transcribed text**
- Dynamically generate questions using **GPT-3.5 / GPT-4**
- Follow-up with clarification questions when needed
- Save structured context to `interview_log.json` and `discovery_output.json`
- **Graceful exit** (user can say "exit" or "cancel")
- Optional **deferred transcription mode**
- 🌐 **Web interface using Flask + Web Audio API** (in progress)

---

## 🗂️ Project Structure

```
Discovery_Voice_App_2/
├── modules/
│   ├── context_manager.py          # Schema + context tracking
│   ├── question_generator.py       # GPT-powered Q&A generation
│   ├── storage.py                  # Save text + audio paths
│   ├── transcribe.py               # Whisper integration (live + file-based)
│   ├── transcribe_all_responses.py# Batch transcribe (optional)
│   └── tts.py                      # Text-to-speech playback
├── responses/                      # Saved audio responses (excluded from git)
├── web/                            # Flask app (MVP UI)
│   ├── app.py                      # Flask backend
│   ├── templates/index.html        # Interview frontend
│   └── static/script.js            # Audio recording + upload
├── interview_log.json              # Structured interview results
├── discovery_output.json           # Final schema context
├── .env                            # OpenAI API key (excluded from git)
├── requirements.txt                # Dependencies
└── main.py                         # Main CLI-driven interview script
```

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/peralese/Discovery_Voice_App_2.git
cd Discovery_Voice_App_2
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your OpenAI API key

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## ▶️ Running the App

### Option A: Terminal-Driven Interview

```bash
python main.py
```

The CLI assistant will:
1. Ask questions using TTS
2. Record microphone input
3. Save response audio
4. Transcribe with Whisper
5. Store results and repeat

---

### Option B: Web Interface (Flask MVP)

```bash
cd web
python app.py
```

Then open: [http://localhost:5000](http://localhost:5000)

You can:
- Hear the current question
- Record and upload audio from your browser
- View live Whisper transcription

---

## 📦 Roadmap

- [x] Voice-based Q&A loop (terminal)
- [x] Whisper-based transcription (CLI + web)
- [x] GPT-driven question generation
- [x] Exit intent detection
- [x] Deferred transcription mode
- [x] Graceful shutdown support
- [x] Web interface MVP (Flask + JS)
- [ ] Dynamic follow-up improvements (soft fix complete)
- [ ] Export summary to CSV / clean JSON
- [ ] Spoken introduction at interview start
- [ ] Pause/resume support
- [ ] End-of-interview summary report
- [ ] Cloud deployment (e.g., Render, EC2, etc.)

---

## 📄 License

MIT License

---

## 👤 Author

**Erick Perales** — *IT Architect, Cloud Migration Specialist*
