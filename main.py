import time
import uuid
import datetime
from modules.context_manager import DiscoveryContext
from modules.question_generator import get_next_question
from modules.tts import speak_text
from modules.transcribe import record_audio_only, transcribe_file_whisper
from modules.storage import save_response

def run_dynamic_interview():
    context = DiscoveryContext()
    last_response = ""

    # ✅ Hardcode the first field: interviewee_name
    if context.get_context()["interviewee_name"] is None:
        first_question = "What is your name?"
        print(f"\n🤖 Question: {first_question}")
        speak_text(first_question)

        audio_path = record_audio_only()
        user_text = transcribe_file_whisper(audio_path)

        # Exit condition
        # if user_text.lower() in ["exit", "quit", "stop", "cancel"]:
        #     print("👋 Interview stopped by user.")
        #     return
        exit_keywords = ["exit", "quit", "stop", "cancel"]
        if any(keyword in user_text.lower() for keyword in exit_keywords):
            print("👋 Detected exit intent in response.")
            save_response("Interview exited by user", user_text, audio_path)
            return



        save_response(first_question, user_text, audio_path)
        context.update_context(user_text)
        last_response = user_text

    while not context.is_complete():
        question = get_next_question(context.get_context(), last_response)
        if not question:
            print("✅ Interview complete.")
            break

        print(f"\n🤖 Question: {question}")
        speak_text(question)

        print("🎙️ Listening for your answer...")
        audio_path = record_audio_only()
        user_text = transcribe_file_whisper(audio_path)

        # if user_text.lower() in ["exit", "quit", "stop", "cancel"]:
        #     print("👋 Interview stopped by user.")
        #     break
        if any(keyword in user_text.lower() for keyword in exit_keywords):
            print("👋 Detected exit intent in response.")
            save_response("Interview exited by user", user_text, audio_path)
            break

        save_response(question, user_text, audio_path)
        context.update_context(user_text)
        last_response = user_text
        time.sleep(1)

    print("\n📄 Final structured context:")
    print(context.to_json())
    context.save_to_file("discovery_output.json")

if __name__ == "__main__":
    run_dynamic_interview()

