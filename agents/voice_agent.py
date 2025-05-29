import requests

def speech_to_text(audio_bytes, elevenlabs_api_key):
    if not elevenlabs_api_key:
        print("ELEVENLABS_API_KEY not provided.")
        return ""
    url = "https://api.elevenlabs.io/v1/speech-to-text"
    headers = {"xi-api-key": elevenlabs_api_key}
    data = {"model_id": "scribe_v1"}
    files = {"file": ("voice_query.wav", audio_bytes, "audio/wav")}
    response = requests.post(url, headers=headers, data=data, files=files)
    print("STT API response:", response.status_code, response.text)  # For debugging
    if response.status_code == 200:
        return response.json().get("text", "")
    return ""

def text_to_speech(text, elevenlabs_api_key, voice_id="tnSpp4vdxKPjI9w0GnoV"):
    if not elevenlabs_api_key:
        print("ELEVENLABS_API_KEY not provided.")
        return None
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": elevenlabs_api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "output_format": "mp3_44100_128",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.7
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    print("TTS API response:", response.status_code, response.text)  # For debugging
    return None
