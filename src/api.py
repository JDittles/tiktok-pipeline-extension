import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from src.pipeline.classify import classify_video, LLMProvider

load_dotenv()

app = FastAPI(
    title="TikTok Crisis Classification API",
    description="Classifies TikTok videos of natural disasters into crisis response taxonomy.",
    version="0.1.0",
)


class ClassifyRequest(BaseModel):
    url: str
    provider: LLMProvider = LLMProvider.GEMINI
    api_key: str | None = None


class ClassifyResponse(BaseModel):
    result: str
    provider: str
    url: str


@app.post("/classify", response_model=ClassifyResponse)
async def classify(req: ClassifyRequest):
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, classify_video, req.url, req.provider, req.api_key
        )
    except Exception as e:
        msg = str(e)
        if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
            raise HTTPException(status_code=429, detail="LLM quota exceeded. Check your API plan and billing.")
        if "401" in msg or "403" in msg or "API_KEY" in msg.upper():
            raise HTTPException(status_code=401, detail="Invalid or missing API key.")
        raise HTTPException(status_code=500, detail=msg)
    return ClassifyResponse(result=result, provider=req.provider.value, url=req.url)


@app.get("/health")
def health():
    return {"status": "ok"}
