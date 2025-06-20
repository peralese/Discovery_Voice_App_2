import time
from modules.context_manager import DiscoveryContext
from modules.question_generator import get_next_question
from modules.tts import speak_text
from modules.transcribe import transcribe_audio_live
from modules.storage import save_response


def run_dynamic_interview():
    context = DiscoveryContext()
    last_response = ""

        # ✅ Hardcode the first field: interviewee_name
    if context.get_context()["interviewee_name"] is None:
        first_question = "What is your name?"
        print(f"\n🤖 Question: {first_question}")
        speak_text(first_question)

        user_text, audio_path = transcribe_audio_live()
        print(f"📝 Transcribed: {user_text}")

        context.update_context(user_text)
        save_response(first_question, user_text, audio_path)
        last_response = user_text

    while not context.is_complete():
        # Ask GPT for next question
        question = get_next_question(context.get_context(), last_response)
        if not question:
            print("✅ Interview complete.")
            break

        print(f"\n🤖 Question: {question}")
        speak_text(question)

        # Get response via mic
        print("🎙️ Listening for your answer...")
        user_text, audio_path = transcribe_audio_live()
        print(f"📝 Transcribed: {user_text}")

        # Update context

    # Final export
    print("\n📄 Final structured context:")
    print(context.to_json())
    context.save_to_file("discovery_output.json")


if __name__ == "__main__":
    run_dynamic_interview()

