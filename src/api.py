from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from src.adaptive_llama_mlx import AdaptiveLlamaProxy
import os

app = FastAPI()
alp = AdaptiveLlamaProxy()

API_KEY = os.environ.get("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key")

async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key

@app.post("/generate")
async def generate(prompt: str, mode: str = "adaptive", api_key: str = Depends(get_api_key)):
    return alp.adaptive_generate(prompt, task_complexity=None if mode == "adaptive" else mode)

@app.get("/stats")
async def get_stats(api_key: str = Depends(get_api_key)):
    return {
        "loaded_models": alp.get_loaded_models(),
        "memory_usage": alp.get_memory_usage()
    }