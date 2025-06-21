import time
import uuid
import datetime
from modules.context_manager import DiscoveryContext
from modules.question_generator import get_next_question
from modules.tts import speak_text
from modules.transcribe import record_audio_only  # <- new function you'll add
from modules.storage import save_response   # <- new function you'll add


def run_dynamic_interview():
    context = DiscoveryContext()
    last_response = ""

    # ✅ Hardcode the first field: interviewee_name
    if context.get_context()["interviewee_name"] is None:
        first_question = "What is your name?"
        print(f"\n🤖 Question: {first_question}")
        speak_text(first_question)

        # audio_path = record_audio_only()
        # save_audio_metadata(first_question, audio_path)
        audio_path = record_audio_only()
        save_response(first_question, "", audio_path)
        last_response = ""
        context.update_context("")  # Empty for now

    while not context.is_complete():
        question = get_next_question(context.get_context(), last_response)
        if not question:
            print("✅ Interview complete.")
            break

        print(f"\n🤖 Question: {question}")
        speak_text(question)

        print("🎙️ Listening for your answer...")
        audio_path = record_audio_only()
        save_response(question, "", audio_path)

        context.update_context("")  # Empty placeholder
        last_response = ""
        time.sleep(1)

    print("\n🎧 Recording complete. Transcription will be run separately.")
    context.save_to_file("discovery_output.json")


if __name__ == "__main__":
    run_dynamic_interview()
