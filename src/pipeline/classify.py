import shutil
import tempfile
from enum import Enum
from langchain.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from .download import download_video
from .video import prepare_gemma4_input
from .prompts import build_prompt


class LLMProvider(Enum):
    OLLAMA = "ollama"
    GEMINI = "gemini"
    OPENAI = "openai"
    CLAUDE = "claude"


_DEFAULT_MODELS = {
    LLMProvider.OLLAMA: "gemma4:e4b",
    LLMProvider.GEMINI: "gemini-2.0-flash",
    LLMProvider.OPENAI: "gpt-4o",
    LLMProvider.CLAUDE: "claude-sonnet-4-6",
}


def classify_video(url: str,
                   provider: LLMProvider = LLMProvider.GEMINI,
                   api_key: str | None = None) -> str:
    model = _DEFAULT_MODELS[provider]

    if provider == LLMProvider.OLLAMA:
        llm = ChatOllama(model=model, temperature=0, max_tokens=2048)
    elif provider == LLMProvider.GEMINI:
        llm = ChatGoogleGenerativeAI(model=model, temperature=0, max_tokens=2048, google_api_key=api_key)
    elif provider == LLMProvider.OPENAI:
        llm = ChatOpenAI(model=model, temperature=0, max_tokens=2048, api_key=api_key)
    elif provider == LLMProvider.CLAUDE:
        llm = ChatAnthropic(model_name=model, temperature=0, max_tokens_to_sample=2048, api_key=api_key)

    tmp_dir = tempfile.mkdtemp()
    try:
        vid_title, vid_desc, vid_id, vid_path = download_video(url, save_dir=tmp_dir)
        vid_elements = prepare_gemma4_input(vid_path)
        prompt = build_prompt(post_title=vid_title, post_desc=vid_desc)
        response = llm.invoke(
            [HumanMessage(content=[{"type": "text", "text": prompt}] + vid_elements)]
        )
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    return response.content
