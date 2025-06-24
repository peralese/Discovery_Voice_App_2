# 🎙️ Voice Interview Bot – Dynamic Q&A Proof of Concept

This project is a proof of concept (PoC) for a **voice-enabled AI interview assistant** designed to gather discovery information from users in a conversational format. It uses speech recognition, text-to-speech, and OpenAI's GPT to guide dynamic interviews.

---

## 🔧 Features

- Ask questions via **text-to-speech (TTS)** using `pyttsx3`
- Voice input with silence detection using `pyaudio`
- Transcribe speech with **OpenAI Whisper API** (replaces Vsok)
- Store both **transcriptions** and **.wav audio files** per question
- Generate questions dynamically using **GPT-3.5 / GPT-4**
- Save structured responses to `interview_log.json` and `discovery_output.json`
- Follow-up questions when clarification is needed

---

## 🗂️ Project Structure

```
Discovery_Voice_App_2/
├── modules/
│   ├── context_manager.py
│   ├── question_generator.py  # (in progress)
│   ├── storage.py # Saves responses with timestamp (in progress)
│   ├── transcribe.py # Microphone input + transcription + audio saving (in progress)
│   └── tts.py # Text-to-Speech playback (in progress)
│   └── transcribe_all_responses.py # Text-to-Speech conversion called at end (in progress)
├── responses/                 # saved audio responses (excluded from git)
├── interview_log.json         # stored structured results (excluded from git)
├── .env                       # OpenAI API key (excluded from git)
├── requirements.txt           (coming soon) 
└── main.py                    # main driver script (in progress)
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

### 4. Download and extract a Vosk model

Download a Vosk English model (e.g., `vosk-model-en-us-0.42-gigaspeech`) from:  
🔗 https://alphacephei.com/vosk/models

Place it in the `models/` directory.

---

### 5. Set your OpenAI API key

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## ▶️ Running the Bot

Run the script:

```bash
python main.py
```

The bot will:
1. Ask the first question via TTS
2. Record your voice answer
3. Transcribe it
4. Store the result
5. Repeat until the schema is complete

---

## 📦 Roadmap

- [x] Voice-based Q&A loop
- [x] Whisper-based transcription
- [x] GPT-driven question generation
- [x] Exit intent recognition
- [x] Deferred transcription mode (optional)
- [ ] Web interface (Flask or Streamlit)
- [ ] Export to CSV / cleaned JSON summary
- [ ] Introductory overview (spoken)
- [ ] Pause/resume support
- [ ] End-of-interview summary report
---

## 📄 License

MIT License

---

## 👤 Author

Erick Perales — *IT Architect, Cloud Migration Specialist*