import speech_recognition as sr

# File name
audio_file = "dummy_audio.wav"
output_file = "audio_to_text.txt"

# Recognizer initialize karo
r = sr.Recognizer()

with sr.AudioFile(audio_file) as source:
    audio_data = r.record(source)   # pura audio read karega
    try:
        # Google Speech Recognition use karo
        text = r.recognize_google(audio_data)

        # Text file me save karo
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)

        print("✅ Audio converted successfully. Saved to", output_file)
    except Exception as e:
        print("❌ Error:", e)
