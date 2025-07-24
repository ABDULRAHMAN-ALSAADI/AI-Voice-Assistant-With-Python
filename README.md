# 🎙️ Voice Assistant using Whisper, Cohere, and pyttsx3

A Python-based voice assistant that listens to your speech, understands it via Whisper and Cohere AI, then responds aloud using pyttsx3 text-to-speech.

## 🚀 Features

- Converts speech to text using OpenAI's Whisper (offline speech recognition)

- Generates AI responses using Cohere’s chat API

- Converts text responses to speech using pyttsx3 (offline TTS engine)

- Continuous conversation flow — listens, responds, speaks, then listens again

- Handles errors gracefully with clear console messages

- No reliance on cloud TTS APIs — all voice output runs locally for instant feedback


## 🛠️ How it works
Record your voice input with the microphone (5 seconds by default)

Transcribe audio to text using Whisper’s speech recognition

Send the text prompt to Cohere’s chat API and receive a smart AI response

Speak the response aloud using pyttsx3 TTS engine

Repeat until you say “quit” or “exit” to stop

## 🐙 Setup & Usage
Requirements
Python 3.8+

Install dependencies:
```bash
pip install cohere whisper sounddevice scipy numpy pyttsx3
```
A Cohere API key — get one for free at [cohere.ai](https://cohere.com/)

## How to run
1- Clone or download the repo

2- Paste your Cohere API key into the script at self.api_key = "your_actual_api_key_here"

3- Run the script:
```bash
python file_name.py
```
4- Speak clearly when prompted

5- The assistant will print your query and respond aloud

## ⚓ Problems Faced while building it & Solutions
- Issue: The assistant spoke only the first response and then stopped talking, only printing text in the terminal for subsequent responses.

- Cause: The pyttsx3 TTS engine was initialized once and reused, which sometimes causes the speech engine to hang or not release audio resources properly.

- Fix: Reinitialize the pyttsx3 engine on every call to speak_text(). Added a short delay after speech to prevent overlap issues. This guaranteed the assistant spoke every response without hanging.

## 🎤 Why these tools?
- Whisper: Offline, high-quality speech recognition, no internet required for STT

- Cohere: Powerful and easy-to-use chat AI, great for conversational responses and free (:

- pyttsx3: Offline, cross-platform TTS engine with no external dependencies, very reliable for speech output

## 📷 Pictures :

<img width="1920" height="1080" alt="Screenshot 2025-07-24 210428" src="https://github.com/user-attachments/assets/b7e6c5a7-0674-450a-bb10-5efc8e3297d1" />


<img width="1920" height="1080" alt="Screenshot 2025-07-24 210548" src="https://github.com/user-attachments/assets/45378ffe-b97e-4e3e-8200-ef222a60087c" />



  ## 🧠 CODE :
  ```python

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
        self.api_key = "your_actual_api_key_here"  # <-- Paste your real key here!
        self.cohere_client = cohere.Client(self.api_key)

        # Load Whisper model
        print("🔍 Loading Whisper model...")
        self.whisper_model = whisper.load_model("base")

       
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

    ```

    
                



  


