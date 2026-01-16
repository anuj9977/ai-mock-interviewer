import requests
import os

HF_API = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"

headers = {
    "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"
}

def speech_to_text(audio_bytes: bytes) -> str:
    response = requests.post(
        HF_API,
        headers=headers,
        data=audio_bytes,
        timeout=60
    )

    result = response.json()
    return result.get("text", "")
