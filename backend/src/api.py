from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from src.adaptive_llama_mlx import AdaptiveLlamaProxy
from pydantic import BaseModel
import os

app = FastAPI()
alp = AdaptiveLlamaProxy()

API_KEY = os.environ.get("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key")

class PromptRequest(BaseModel):
    prompt: str
    model: str = "full"

async def get_api_key(api_key: str = Depends(api_key_header)):
    if API_KEY and api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key

@app.post("/generate")
async def generate(request: PromptRequest, api_key: str = Depends(get_api_key)):
    result = alp.adaptive_generate(request.prompt, task_complexity=request.model if request.model != "full" else None)
    metrics = alp.get_metrics()
    
    return {
        "response": result["response"],
        "model": result["model_used"],
        "metrics": {
            "latency": result["generation_time"],
            "memoryUsage": result["memory_usage"],
            "taskComplexity": result["task_complexity"],
            "modelUsage": metrics["modelUsage"],
            "memorySavings": result["memory_saved"],
        }
    }

@app.get("/stats")
async def get_stats(api_key: str = Depends(get_api_key)):
    metrics = alp.get_metrics()
    return {
        "loaded_models": alp.get_loaded_models(),
        "memory_usage": alp.get_memory_usage(),
        "total_requests": metrics["totalRequests"],
        "total_memory_saved": metrics["totalMemorySaved"],
        "model_usage": metrics["modelUsage"]
    }