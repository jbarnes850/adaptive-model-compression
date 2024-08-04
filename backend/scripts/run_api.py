import uvicorn
import os

if __name__ == "__main__":
    if not os.environ.get("API_KEY"):
        print("Warning: API_KEY environment variable not set. API will be unsecured.")
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)