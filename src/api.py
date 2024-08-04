from fastapi import FastAPI
from src.adaptive_llama_mlx import AdaptiveLlamaProxy

app = FastAPI()
alp = AdaptiveLlamaProxy()

@app.post("/generate")
async def generate(prompt: str, mode: str = "adaptive"):
    return alp.adaptive_generate(prompt, task_complexity=None if mode == "adaptive" else mode)

@app.get("/stats")
async def get_stats():
    return {
        "loaded_models": alp.get_loaded_models(),
        "memory_usage": alp.get_memory_usage()
    }