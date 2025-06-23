import os
import wave
import uuid
import pyaudio
import time
from dotenv import load_dotenv
from openai import OpenAI

# --- Load API key ---
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Audio config ---
AUDIO_DIR = "responses"
RATE = 16000
CHUNK = 4000
CHANNELS = 1
FORMAT = pyaudio.paInt16
SILENCE_THRESHOLD = 4  # seconds

# Ensure responses directory exists
os.makedirs(AUDIO_DIR, exist_ok=True)

# -------------------------------
# 🎙️ RECORD AUDIO TO .WAV FILE
# -------------------------------
def record_audio_only():
    audio_filename = os.path.join(AUDIO_DIR, f"response_{uuid.uuid4().hex}.wav")

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print(f"🎙️ Recording... Speak now. Silence for {SILENCE_THRESHOLD}s will stop recording.")
    frames = []
    start_time = time.time()
    last_spoken_time = start_time

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

            # crude silence detection
            if any(abs(x) > 500 for x in memoryview(data).cast('h')):
                last_spoken_time = time.time()

            if time.time() - last_spoken_time > SILENCE_THRESHOLD:
                print("🤫 Silence detected. Ending recording.")
                break

    except KeyboardInterrupt:
        print("⏹️ Recording interrupted by user.")

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(audio_filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    print(f"💾 Audio saved: {audio_filename}")
    return audio_filename


# -------------------------------
# 🤖 TRANSCRIBE USING WHISPER API
# -------------------------------
def transcribe_file_whisper(path):
    with open(path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
    )
    return transcript.strip()
