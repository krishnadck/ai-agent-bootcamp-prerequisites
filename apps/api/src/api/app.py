from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel

from openai import OpenAI
from google import genai
from groq import Groq

from api.core.config import config
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def run_llm(provider, model_name, messages, max_tokens=500):
    if provider == "openai":
        client = OpenAI(api_key=config.openai_api_key)
    elif provider == "google":
        client = genai.Client(api_key=config.google_api_key)
    elif provider == "groq":
        client = Groq(api_key=config.groq_api_key)
    else:
        raise ValueError(f"Invalid provider: {provider}")

    
    if provider == "google":
        return client.models.generate_content(
            model=model_name,
            contents=[message["content"] for message in messages],
        ).text
    elif provider == "groq":
        return client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_completion_tokens=max_tokens,
        ).choices[0].message.content
    else:
        return client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_completion_tokens=max_tokens,
            reasoning_effort="minimal",
        ).choices[0].message.content

class ChatRequest(BaseModel):
    provider: str
    model_name: str
    messages: list[dict]

class ChatResponse(BaseModel):
    message: str

app = FastAPI()

@app.post("/chat")
async def chat(request: Request, payload: ChatRequest) -> ChatResponse:
    try:
        response = run_llm(payload.provider, payload.model_name, payload.messages)
        return ChatResponse(message=response)
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))