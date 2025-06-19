import time
from modules.context_manager import DiscoveryContext
from modules.question_generator import get_next_question
from modules.tts import speak_text
from modules.transcribe import transcribe_audio_live
from modules.storage import save_response


def run_dynamic_interview():
    context = DiscoveryContext()
    last_response = ""

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
        context.update_context(user_text)

        # Save current response (optional logging)
        save_response(question, user_text)
        last_response = user_text
        time.sleep(1)

    # Final export
    print("\n📄 Final structured context:")
    print(context.to_json())
    context.save_to_file("discovery_output.json")


if __name__ == "__main__":
    run_dynamic_interview()

