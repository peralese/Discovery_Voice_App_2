import pyttsx3

# Initialize the TTS engine once
_engine = pyttsx3.init()
_engine.setProperty('rate', 150)  # Set speaking rate

def speak_text(text):
    """
    Convert input text to speech and play it aloud.
    """
    print(f"🗣️ Speaking: {text}")
    _engine.say(text)
    _engine.runAndWait()
