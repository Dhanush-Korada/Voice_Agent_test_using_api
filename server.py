from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from google import genai
from google.genai import types


PROJECT_DIR = Path(__file__).resolve().parent
STATIC_DIR = PROJECT_DIR / "static"
load_dotenv(PROJECT_DIR / ".env")

GEMINI_LIVE_MODELS = [
    "gemini-3.8-live",
    "gemini-3.1-flash-live-preview",
    "gemini-2.5-flash-native-audio-preview-12-2025",
]

SYSTEM_INSTRUCTION = """You are Dhanush AI, a realtime voice assistant.

Understand English and Telugu.

If the user speaks Telugu, respond naturally in Telugu.
If the user speaks English, respond naturally in English.
If the user mixes Telugu and English, respond naturally in the same mixed style.

The user may switch languages at any time.

Keep answers concise and natural.
Speak like a helpful realtime voice assistant.
Do not pretend to be human.
Do not claim to have performed an action unless you actually performed it."""

app = FastAPI(title="Dhanush AI Voice Agent")


def _auto_fallback_enabled() -> bool:
    return os.getenv("GEMINI_AUTO_FALLBACK", "true").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def _model_candidates() -> list[str]:
    configured_model = os.getenv("GEMINI_MODEL", "").strip()
    candidates = [configured_model] if configured_model else [GEMINI_LIVE_MODELS[0]]
    if _auto_fallback_enabled():
        candidates.extend(GEMINI_LIVE_MODELS)
    return list(dict.fromkeys(candidates))


def _client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key == "YOUR_GEMINI_API_KEY":
        raise HTTPException(
            status_code=503,
            detail="GEMINI_API_KEY is missing. Add your key to the project's .env file and restart the server.",
        )
    return genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(api_version="v1beta"),
    )


def _live_config() -> types.LiveConnectConfig:
    voice = os.getenv("GEMINI_VOICE", "Puck").strip() or "Puck"
    return types.LiveConnectConfig(
        response_modalities=["AUDIO"],
        system_instruction=SYSTEM_INSTRUCTION,
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice)
            )
        ),
        input_audio_transcription=types.AudioTranscriptionConfig(),
        output_audio_transcription=types.AudioTranscriptionConfig(),
    )


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/token")
async def create_token(model: str | None = Query(default=None)) -> dict[str, object]:
    candidates = _model_candidates()
    selected_model = model or candidates[0]
    if selected_model not in candidates:
        raise HTTPException(status_code=400, detail="Requested model is not in the configured Live model list.")

    client = _client()
    now = datetime.now(timezone.utc)
    try:
        token = client.auth_tokens.create(
            config=types.CreateAuthTokenConfig(
                uses=1,
                expire_time=now + timedelta(minutes=30),
                new_session_expire_time=now + timedelta(minutes=2),
                live_connect_constraints=types.LiveConnectConstraints(
                    model=selected_model,
                    config=_live_config(),
                ),
            )
        )
    except Exception as exc:
        message = str(exc)
        status_code = 400 if any(
            marker in message.lower()
            for marker in ("model", "unsupported", "not found", "not_found")
        ) else 502
        raise HTTPException(status_code=status_code, detail=message) from exc

    token_value = getattr(token, "name", None)
    if not token_value:
        raise HTTPException(
            status_code=502,
            detail="Google did not return an ephemeral token. Check that the GenAI SDK and Live API are available.",
        )
    return {
        "token": token_value,
        "model": selected_model,
        "models": candidates,
        "voice": os.getenv("GEMINI_VOICE", "Puck").strip() or "Puck",
        "apiVersion": "v1beta",
    }


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")