from gtts import gTTS
import tempfile
import os

def text_to_speech(text: str) -> bytes:
    """
    Convert text to speech and return audio bytes
    """
    tts = gTTS(text)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tts.save(tmp.name)
        tmp_path = tmp.name

    with open(tmp_path, "rb") as f:
        audio_bytes = f.read()

    os.remove(tmp_path)
    return audio_bytes
