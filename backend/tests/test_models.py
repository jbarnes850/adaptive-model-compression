import os
import sys
import time
import argparse
from mlx_lm import load, generate
from tqdm import tqdm

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.adaptive_llama_mlx import AdaptiveLlamaProxy

def download_and_test_model(model_path, model_name):
    print(f"Downloading and testing {model_name} model...")
    start_time = time.time()
    
    try:
        with tqdm(total=100, desc=f"Loading {model_name} model", unit="%") as pbar:
            model, tokenizer = load(model_path)
            pbar.update(100)
        print(f"{model_name} model loaded successfully.")
        
        # Test the model with a simple prompt
        test_prompt = "Hello, how are you?"
        response = generate(model, tokenizer, prompt=test_prompt, verbose=False)
        print(f"Test response from {model_name} model: {response}")
        
        end_time = time.time()
        print(f"{model_name} model download and test completed in {end_time - start_time:.2f} seconds.")
        print("--------------------")
    except Exception as e:
        print(f"Error downloading or testing {model_name} model: {str(e)}")
        print("--------------------")

def main():
    parser = argparse.ArgumentParser(description="Download and test MLX models")
    parser.add_argument("model", choices=["simple", "medium", "complex", "all"], 
                        help="Which model to download and test")
    args = parser.parse_args()

    alp = AdaptiveLlamaProxy()
    
    if args.model == "all":
        for complexity, model_path in alp.model_paths.items():
            download_and_test_model(model_path, complexity)
    else:
        model_path = alp.model_paths[args.model]
        download_and_test_model(model_path, args.model)

if __name__ == "__main__":
    main()