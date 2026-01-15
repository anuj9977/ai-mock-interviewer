import os
import tempfile
import subprocess
import numpy as np
import soundfile as sf
import whisper

# Load model once
model = whisper.load_model("base")

FFMPEG_PATH = r"C:\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"

def speech_to_text(audio_bytes: bytes) -> str:
    print("🎧 Audio bytes received:", len(audio_bytes))

    # Save browser audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        tmp.write(audio_bytes)
        webm_path = tmp.name

    wav_path = webm_path.replace(".webm", ".wav")

    # Convert to WAV using explicit ffmpeg
    subprocess.run(
        [
            FFMPEG_PATH,
            "-y",
            "-i",
            webm_path,
            "-ar", "16000",
            "-ac", "1",
            wav_path,
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # 🔥 LOAD AUDIO OURSELVES (NO WHISPER FFMPEG)
    audio, sr = sf.read(wav_path)
    if sr != 16000:
        raise ValueError("Sample rate mismatch")

    # Convert to float32 numpy
    audio = audio.astype(np.float32)

    # Transcribe using raw audio array
    result = model.transcribe(audio)

    # Cleanup
    os.remove(webm_path)
    os.remove(wav_path)

    return result["text"].strip()
