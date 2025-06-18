# 🎙️ Voice Interview Bot – Dynamic Q&A Proof of Concept

This project is a proof of concept (PoC) for a **voice-enabled AI interview assistant** designed to gather discovery information from users in a conversational format. It uses speech recognition, text-to-speech, and OpenAI's GPT to guide dynamic interviews.

---

## 🔧 Features

- Ask questions via **text-to-speech (TTS)** using `pyttsx3`
- Record spoken answers via `pyaudio` and transcribe them with `Vosk`
- Store both **transcriptions** and **audio files** per question
- Generate questions dynamically (coming soon via GPT-4 integration)
- Store structured responses to a `interview_log.json` file

---

## 🗂️ Project Structure

```
Discovery_Voice_App_2/
├── modules/
│   ├── context_manager.py
│   ├── question_generator.py  # (in progress)
│   └── storage.py # (coming soon)
├── responses/                 # saved audio responses (coming soon)
├── models/                    # Vosk model (e.g., vosk-model-en-us-0.42-gigaspeech) (coming soon)
├── questions.json             # base schema for interview (coming soon)
├── interview_log.json         # stored structured results (coming soon)
├── .env                       # OpenAI API key (excluded from git)
├── requirements.txt           (coming soon) 
└── main.py                    # main driver script (coming soon)
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

- [ ] Voice question + voice response capture
- [ ] Save transcriptions and audio
- [x] Structured context manager
- [ ] Dynamic question generation (GPT-based)
- [ ] Web interface (streamlit or flask)

---

## 📄 License

MIT License

---

## 👤 Author

Erick Perales — *IT Architect, Cloud Migration Specialist*