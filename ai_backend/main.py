import os
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = [
    "https://cms-phy-det-analysis.docs.cern.ch",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"status": "ok", "service": "cms-phy-det-analysis-ai-backend"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/chat")
async def chat(request: ChatRequest):
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        return {
            "answer": "DEEPSEEK_API_KEY is not configured.",
            "deepseek_api_key_configured": False,
            "model": "deepseek-v4-flash",
            "sources": []
        }

    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-v4-flash",
        "messages": [
            {
                "role": "system",
                "content": "You are an AI assistant for lichengz's CERN detector analysis website. For now, answer normally and briefly. Later you will answer using retrieved website context."
            },
            {
                "role": "user",
                "content": request.question
            }
        ],
        "temperature": 0.3,
        "stream": False
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload, timeout=30.0)
            
            if response.status_code != 200:
                # Do not expose the API key in the error message
                return {
                    "answer": f"API request failed with status code {response.status_code}: {response.text}",
                    "deepseek_api_key_configured": True,
                    "model": "deepseek-v4-flash",
                    "sources": []
                }
            
            data = response.json()
            answer = data["choices"][0]["message"]["content"]
            
            return {
                "answer": answer,
                "deepseek_api_key_configured": True,
                "model": "deepseek-v4-flash",
                "sources": []
            }
    except Exception as e:
        return {
            "answer": f"An error occurred while calling the API: {str(e)}",
            "deepseek_api_key_configured": True,
            "model": "deepseek-v4-flash",
            "sources": []
        }
