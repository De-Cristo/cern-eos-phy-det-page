import os
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
def chat(request: ChatRequest):
    kimi_api_key_exists = "KIMI_API_KEY" in os.environ
    return {
        "answer": f"Backend received your question: {request.question}",
        "kimi_api_key_configured": kimi_api_key_exists,
        "sources": []
    }
