import requests
import base64

def process_text_query(query):
    response = requests.post("http://localhost:8000/process-query/", params={"query": query})
    result = response.json()
    audio_bytes = base64.b64decode(result["audio_b64"]) if result["audio_b64"] else None
    return {"text": result["text"], "audio_bytes": audio_bytes, "logs": result.get("logs", [])}

def process_voice_query(audio_bytes):
    files = {"audio": ("voice_query.wav", audio_bytes, "audio/wav")}
    response = requests.post("http://localhost:8000/process-voice/", files=files)
    result = response.json()
    audio_bytes = base64.b64decode(result["audio_b64"]) if result["audio_b64"] else None
    return {"text": result["text"], "audio_bytes": audio_bytes, "logs": result.get("logs", [])}
