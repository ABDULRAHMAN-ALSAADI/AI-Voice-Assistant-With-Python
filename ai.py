import os
import time
import cohere
import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import pyttsx3
import tempfile

class VoiceAssistant:
    def __init__(self):
        # 🔐 Hardcoded Cohere API key (⚠️ only for local dev)
        self.api_key = "ISV45D1V0LcPBybHcW295JPQ7t4Bwu8N90hkbiYt"  # <-- Paste your real key here!
        self.cohere_client = cohere.Client(self.api_key)

        # Load Whisper model
        print("🔍 Loading Whisper model...")
        self.whisper_model = whisper.load_model("base")

        # Removed persistent TTS engine here to fix hangups

    def record_audio(self, duration=5, fs=16000):
        print("🎙️ Recording... Speak now!")
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        return fs, audio

    def save_audio_to_wav(self, fs, audio):
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        wav.write(temp_file.name, fs, audio)
        return temp_file.name

    def transcribe_audio(self, file_path):
        print("🧠 Transcribing...")
        result = self.whisper_model.transcribe(file_path)
        return result["text"].strip()

    def generate_response(self, prompt: str):
        print("🤖 Generating response...")
        try:
            response = self.cohere_client.chat(
                message=prompt,
                model="command-r-plus",
                temperature=0.7
            )
            return response.text.strip()
        except Exception as e:
            print(f"❌ Cohere Error: {e}")
            return "Sorry, I couldn't understand that."

    def speak_text(self, text):
        try:
            print(f"🔊 Speaking: {text}")
            # Create a new TTS engine instance each call to avoid hangups
            tts_engine = pyttsx3.init()
            tts_engine.setProperty('rate', 160)
            tts_engine.say(text)
            tts_engine.runAndWait()
            tts_engine.stop()
            print("✅ Done speaking")
            time.sleep(0.3)  # Small pause to avoid overlapping audio issues
        except Exception as e:
            print(f"❌ TTS Error: {e}")

    def run(self):
        print("="*50)
        print("🎤 Voice Assistant Using Whisper + Cohere + pyttsx3")
        print("Say 'quit' to exit")
        print("="*50)

        while True:
            try:
                fs, audio = self.record_audio(duration=5)
                audio_file = self.save_audio_to_wav(fs, audio)
                user_text = self.transcribe_audio(audio_file)

                if not user_text:
                    print("❓ Didn't catch that. Try again.")
                    continue

                print(f"👤 You said: {user_text}")

                if user_text.lower() in ["quit", "exit", "stop"]:
                    self.speak_text("Goodbye!")
                    break

                response = self.generate_response(user_text)
                print(f"🤖 Assistant: {response}")
                self.speak_text(response)

            except Exception as e:
                print(f"💥 Error: {e}")
                self.speak_text("Something went wrong.")

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()
