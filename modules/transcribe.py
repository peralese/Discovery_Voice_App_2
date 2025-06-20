import os
import wave
import uuid
import pyaudio
import time
from vosk import Model, KaldiRecognizer
import json

# Configuration
AUDIO_DIR = "responses"
RATE = 16000
CHUNK = 4000
CHANNELS = 1
FORMAT = pyaudio.paInt16
MODEL_PATH = "models/vosk-model-en-us-0.42-gigaspeech"
SILENCE_THRESHOLD = 6  # seconds of silence to stop recording

# Ensure audio directory exists
os.makedirs(AUDIO_DIR, exist_ok=True)

# Load Vosk model once
model = Model(MODEL_PATH)

def transcribe_audio_live():
    recognizer = KaldiRecognizer(model, RATE)
    audio_filename = os.path.join(AUDIO_DIR, f"response_{uuid.uuid4().hex}.wav")

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print(f"🎙️ Recording... Speak now. Silence for {SILENCE_THRESHOLD}s will stop recording.")
    frames = []
    text = ""
    partial_text = ""
    start_time = time.time()
    last_spoken_time = start_time

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                spoken = result.get("text", "").strip()
                if spoken:
                    text += spoken + " "
                    last_spoken_time = time.time()
            else:
                partial = json.loads(recognizer.PartialResult()).get("partial", "").strip()
                if partial:
                    partial_text = partial  # Save last partial words

            if time.time() - last_spoken_time > SILENCE_THRESHOLD:
                print("🤫 Silence detected. Ending recording.")
                break

    except KeyboardInterrupt:
        print("⏹️ Recording interrupted by user.")
        text = "[Interrupted]"

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Save the audio
        wf = wave.open(audio_filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        print(f"💾 Audio saved: {audio_filename}")

    # If full result is blank, use last partial fallback
    final_text = text.strip() or partial_text.strip()
    return final_text, audio_filename
