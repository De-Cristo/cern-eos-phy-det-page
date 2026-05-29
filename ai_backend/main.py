import os
import httpx
import logging
import re
import asyncio
import json
from typing import List, Dict, Optional
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

RAG_INDEX_URL = os.environ.get("RAG_INDEX_URL", "https://cms-phy-det-analysis.docs.cern.ch/ai_index/chunks.jsonl")
RAG_TOP_K = int(os.environ.get("RAG_TOP_K", 6))

class RagCache:
    def __init__(self):
        self.chunks = []
        self.loaded = False
        self.loading = False
        self.lock = asyncio.Lock()

rag_cache = RagCache()

async def load_rag_chunks():
    if rag_cache.loaded or rag_cache.loading:
        return
    
    async with rag_cache.lock:
        if rag_cache.loaded:
            return
        rag_cache.loading = True
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(RAG_INDEX_URL, timeout=15.0)
                if response.status_code == 200:
                    chunks = []
                    for line in response.text.strip().split("\n"):
                        if line:
                            chunks.append(json.loads(line))
                    rag_cache.chunks = chunks
                    rag_cache.loaded = True
                    logging.info(f"Loaded {len(chunks)} chunks from RAG_INDEX_URL")
                else:
                    logging.warning(f"Failed to load RAG index: HTTP {response.status_code}")
        except Exception as e:
            logging.error(f"Error loading RAG index: {e}")
        finally:
            rag_cache.loading = False

def search_chunks(query: str, top_k: int = RAG_TOP_K) -> List[Dict]:
    if not rag_cache.loaded or not rag_cache.chunks:
        return []
    
    query_terms = set(re.findall(r'\w+', query.lower()))
    if not query_terms:
        return []
    
    scored_chunks = []
    for chunk in rag_cache.chunks:
        score = 0
        text_lower = chunk['text'].lower()
        title_lower = chunk.get('title', '').lower()
        path_lower = chunk.get('source_path', '').lower()
        
        for term in query_terms:
            if term in text_lower:
                score += 1
            if term in title_lower:
                score += 2
            if term in path_lower:
                score += 2
        
        if score > 0:
            scored_chunks.append((score, chunk))
    
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    return [c for score, c in scored_chunks[:top_k]]

class ChatRequest(BaseModel):
    question: str

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(load_rag_chunks())

@app.get("/")
def read_root():
    return {"status": "ok", "service": "cms-phy-det-analysis-ai-backend"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/version")
def version():
    return {
        "backend": "ai-backend",
        "provider": "deepseek",
        "model": "deepseek-v4-flash",
        "code_version": "deepseek-v4-flash-001",
        "rag": "lexical-v0"
    }

@app.get("/rag/status")
async def rag_status():
    if not rag_cache.loaded:
        await load_rag_chunks()
    return {
        "rag_enabled": rag_cache.loaded and len(rag_cache.chunks) > 0,
        "index_url": RAG_INDEX_URL,
        "chunks_loaded": len(rag_cache.chunks)
    }

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

    await load_rag_chunks()
    
    relevant_chunks = search_chunks(request.question)
    
    system_prompt = "You are an AI assistant for lichengz's CERN detector analysis website.\nUse the provided website context when relevant.\nIf the context is insufficient, say so.\nCite sources using [1], [2], etc."
    
    if relevant_chunks:
        context_blocks = []
        for i, chunk in enumerate(relevant_chunks, 1):
            context_blocks.append(f"[{i}] Title: {chunk.get('title', 'Unknown')}\nURL: {chunk.get('source_url', '')}\nText: {chunk['text']}")
        
        system_prompt += "\n\nWebsite Context:\n" + "\n\n".join(context_blocks)

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
                "content": system_prompt
            },
            {
                "role": "user",
                "content": request.question
            }
        ],
        "temperature": 0.3,
        "stream": False
    }

    sources_out = []
    for i, chunk in enumerate(relevant_chunks, 1):
        sources_out.append({
            "id": i,
            "title": chunk.get('title', 'Unknown'),
            "url": chunk.get('source_url', ''),
            "source_path": chunk.get('source_path', '')
        })

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload, timeout=30.0)
            
            if response.status_code != 200:
                return {
                    "answer": f"API request failed with status code {response.status_code}",
                    "deepseek_api_key_configured": True,
                    "model": "deepseek-v4-flash",
                    "sources": sources_out
                }
            
            data = response.json()
            answer = data["choices"][0]["message"]["content"]
            
            if not relevant_chunks and not rag_cache.loaded:
                answer += "\n\n(Warning: RAG index could not be loaded.)"

            return {
                "answer": answer,
                "deepseek_api_key_configured": True,
                "model": "deepseek-v4-flash",
                "sources": sources_out
            }
    except Exception as e:
        return {
            "answer": f"An error occurred while calling the API: {str(e)}",
            "deepseek_api_key_configured": True,
            "model": "deepseek-v4-flash",
            "sources": sources_out
        }
