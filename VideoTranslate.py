# %%
import subprocess
import os
import whisper
from TTS.api import TTS
# %%
# CONFIG
VIDEO_PATH = "ChineseSong.MP4"
WORK_DIR = "Output"

AUDIO_PATH = os.path.join(WORK_DIR, "song.wav")
ENGLISH_VOICE_PATH = os.path.join(WORK_DIR, "english_voice.wav")

CHINESE_TEXT_PATH = os.path.join(WORK_DIR, "lyrics_zh.txt")
ENGLISH_TEXT_PATH = os.path.join(WORK_DIR, "lyrics_en.txt")
COMPARISON_PATH = os.path.join(WORK_DIR, "lyrics_zh_en_comparison.txt")

os.makedirs(WORK_DIR, exist_ok=True)
# %%
# EXTRACT AUDIO FROM VIDEO
print("Extracting audio from video...")

cmd = [
    "ffmpeg",
    "-y",
    "-i", VIDEO_PATH,
    "-vn",
    "-acodec", "pcm_s16le",
    "-ar", "44100",
    "-ac", "1",
    AUDIO_PATH
]

subprocess.run(cmd, check=True)

print(f"Audio saved to: {AUDIO_PATH}")
# %%
# TRANSCRIBE CHINESE (ORIGINAL)
print("Loading Whisper model...")
model = whisper.load_model("medium") 

print("Transcribing Chinese singing...")
zh_result = model.transcribe(
    AUDIO_PATH,
    task="transcribe",
    language="zh"
)

chinese_text = zh_result["text"]

print("\n--- Chinese Transcription ---")
print(chinese_text)

# with open(CHINESE_TEXT_PATH, "w", encoding="utf-8") as f:
#     f.write(chinese_text)
# %%
# TRANSLATE CHINESE → ENGLISH
print("Translating to English...")
en_result = model.transcribe(
    AUDIO_PATH,
    task="translate",
    language="zh"
)

english_text = en_result["text"]

print("\n--- English Translation ---")
print(english_text)

# with open(ENGLISH_TEXT_PATH, "w", encoding="utf-8") as f:
#     f.write(english_text)
# %%
# SAVE LINE-BY-LINE CHINESE ↔ ENGLISH COMPARISON
zh_segments = zh_result["segments"]
en_segments = en_result["segments"]

lines = []

for i, (zh, en) in enumerate(zip(zh_segments, en_segments), start=1):
    zh_text = zh["text"].strip()
    en_text = en["text"].strip()

    if zh_text and en_text:
        lines.append(f"{i}. {zh_text}")
        lines.append(f"   {en_text}")
        lines.append("")  

comparison_text = "\n".join(lines)

with open(COMPARISON_PATH, "w", encoding="utf-8") as f:
    f.write(comparison_text)

print(f"Saved line-by-line comparison to: {COMPARISON_PATH}")

# %%
# TEXT TO SPEECH (ENGLISH)
print("Generating English voice audio...")

tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

tts.tts_to_file(
    text=english_text,
    file_path=ENGLISH_VOICE_PATH
)

print(f"English voice saved to: {ENGLISH_VOICE_PATH}")
print("Pipeline complete.")
