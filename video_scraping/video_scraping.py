import subprocess
import speech_recognition as sr

video_file = "dummy video.mp4"
audio_file = "audio.wav"
output_file = "video_text.txt"

# 1. Video se audio extract (PCM WAV format me)
subprocess.run([
    "ffmpeg", "-y", "-i", video_file,
    "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
    audio_file
])

# 2. Speech recognizer initialize
r = sr.Recognizer()

with sr.AudioFile(audio_file) as source:
    audio = r.record(source)   # pura audio read karega

try:
    # Google Speech Recognition
    text = r.recognize_google(audio)

    # Output file me save karo
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)

    print("✅ Transcript saved in", output_file)

except Exception as e:
    print("❌ Error:", e)
