from fastapi import FastAPI, UploadFile, File, Form
from orchestrator.rag_orchestrator import orchestrate
from agents.voice_agent import speech_to_text
import base64

app = FastAPI()

@app.post("/process-query/")
async def process_query(
    query: str = Form(...),
    gemini_api_key: str = Form(...),
    elevenlabs_api_key: str = Form(...),
    voice_id: str = Form("tnSpp4vdxKPjI9w0GnoV")
):
    result = orchestrate(query, gemini_api_key, elevenlabs_api_key, voice_id)
    # For audio, encode as base64 for JSON transport
    audio_b64 = base64.b64encode(result["audio_bytes"]).decode() if result["audio_bytes"] else ""
    return {
        "text": result["text"],
        "audio_b64": audio_b64,
        "logs": result.get("logs", []),
        "plan": result.get("plan", []),
        "data": result.get("data", {})
    }

@app.post("/process-voice/")
async def process_voice(
    audio: UploadFile = File(...),
    gemini_api_key: str = Form(...),
    elevenlabs_api_key: str = Form(...),
    voice_id: str = Form("tnSpp4vdxKPjI9w0GnoV")
):
    audio_bytes = await audio.read()
    query = speech_to_text(audio_bytes, elevenlabs_api_key)
    result = orchestrate(query, gemini_api_key, elevenlabs_api_key, voice_id)
    audio_b64 = base64.b64encode(result["audio_bytes"]).decode() if result["audio_bytes"] else ""
    return {
        "text": result["text"],
        "audio_b64": audio_b64,
        "logs": result.get("logs", []),
        "plan": result.get("plan", []),
        "data": result.get("data", {})
    }
