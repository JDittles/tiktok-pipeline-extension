import asyncio
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from dotenv import load_dotenv
from src.pipeline.classify import classify_video, LLMProvider

load_dotenv()

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="TikTok Crisis Classification API",
    description="Classifies TikTok videos of natural disasters into crisis response taxonomy.",
    version="0.1.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)

_DEMO_PROVIDER = LLMProvider.CLAUDE

_ENV_KEYS = {
    LLMProvider.GEMINI: "GEMINI_API_KEY",
    LLMProvider.OPENAI: "OPENAI_API_KEY",
    LLMProvider.CLAUDE: "ANTHROPIC_API_KEY",
}


class ClassifyRequest(BaseModel):
    url: str
    provider: LLMProvider = LLMProvider.GEMINI
    api_key: str | None = None


class ClassifyDemoRequest(BaseModel):
    url: str


class ClassifyResponse(BaseModel):
    result: str
    provider: str
    url: str


async def _classify(url: str, provider: LLMProvider, api_key: str | None) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, classify_video, url, provider, api_key)


def _handle_llm_error(e: Exception) -> None:
    msg = str(e)
    if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
        raise HTTPException(status_code=429, detail="LLM quota exceeded. Check your API plan and billing.")
    if "401" in msg or "403" in msg or "API_KEY" in msg.upper():
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")
    raise HTTPException(status_code=500, detail=msg)


@app.post("/classify", response_model=ClassifyResponse)
async def classify(req: ClassifyRequest):
    try:
        result = await _classify(req.url, req.provider, req.api_key)
    except HTTPException:
        raise
    except Exception as e:
        _handle_llm_error(e)
        raise  # unreachable, satisfies type checker
    return ClassifyResponse(result=result, provider=req.provider.value, url=req.url)


@app.post("/classify/demo", response_model=ClassifyResponse)
@limiter.limit("5/hour")
async def classify_demo(request: Request, req: ClassifyDemoRequest):  # request required by slowapi
    api_key = os.getenv(_ENV_KEYS[_DEMO_PROVIDER])
    if not api_key:
        raise HTTPException(status_code=503, detail="Demo unavailable.")
    try:
        result = await _classify(req.url, _DEMO_PROVIDER, api_key)
    except HTTPException:
        raise
    except Exception as e:
        _handle_llm_error(e)
        raise  # unreachable, satisfies type checker
    return ClassifyResponse(result=result, provider=_DEMO_PROVIDER.value, url=req.url)


@app.get("/health")
def health():
    return {"status": "ok"}
