import requests
import base64

# Set your deployed FastAPI backend URL here
BACKEND_URL = "https://finance-assisstant.onrender.com"

def process_text_query(query, gemini_api_key, elevenlabs_api_key, voice_id):
    data = {
        "query": query,
        "gemini_api_key": gemini_api_key,
        "elevenlabs_api_key": elevenlabs_api_key,
        "voice_id": voice_id
    }
    response = requests.post(f"{BACKEND_URL}/process-query/", data=data)
    result = response.json()
    audio_bytes = base64.b64decode(result["audio_b64"]) if result.get("audio_b64") else None
    return {
        "text": result["text"],
        "audio_bytes": audio_bytes,
        "logs": result.get("logs", []),
        "plan": result.get("plan", []),
        "data": result.get("data", {})
    }

def process_voice_query(audio_bytes, gemini_api_key, elevenlabs_api_key, voice_id):
    files = {"audio": ("voice_query.wav", audio_bytes, "audio/wav")}
    data = {
        "gemini_api_key": gemini_api_key,
        "elevenlabs_api_key": elevenlabs_api_key,
        "voice_id": voice_id
    }
    response = requests.post(f"{BACKEND_URL}/process-voice/", files=files, data=data)
    result = response.json()
    audio_bytes = base64.b64decode(result["audio_b64"]) if result.get("audio_b64") else None
    return {
        "text": result["text"],
        "audio_bytes": audio_bytes,
        "logs": result.get("logs", []),
        "plan": result.get("plan", []),
        "data": result.get("data", {})
    }
