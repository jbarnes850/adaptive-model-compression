"""
This script evaluates the Adaptive LLaMA Proxy model on a diverse dataset.

To run this script, use the following command from the project root directory:
python3 backend/scripts/evaluate_model.py

This script will:
1. Evaluate the adaptive system
2. Evaluate the full model baseline
3. Evaluate the compressed model baseline
4. Plot and save comparison results
5. Run a long-term test (24 hours by default)
6. Plot and save long-term test results
7. Print model sizes

Note: This script may take a considerable amount of time to run, especially the long-term test.
"""

import sys
import os
import time
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
import warnings
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('wordnet', quiet=True)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings("ignore", message="None of PyTorch, TensorFlow >= 2.0, or Flax have been found.")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.adaptive_llama_mlx import AdaptiveLlamaProxy
from src.utils import create_diverse_dataset

def evaluate_model(alp, dataset, mode='adaptive'):
    results = {
        'very_simple': {'accuracy': 0, 'latency': 0, 'memory': 0},
        'simple': {'accuracy': 0, 'latency': 0, 'memory': 0},
        'medium': {'accuracy': 0, 'latency': 0, 'memory': 0},
        'complex': {'accuracy': 0, 'latency': 0, 'memory': 0}
    }
    
    for item in tqdm(dataset, desc=f"Evaluating {mode} mode"):
        response = alp.adaptive_generate(item['input'], task_complexity=None if mode == 'adaptive' else mode)
        
        complexity = response['task_complexity']
        latency = response['generation_time']
        memory = response['memory_usage']
        
        accuracy = 1 if item['target'] in response['response'] else 0
        
        results[complexity]['accuracy'] += accuracy
        results[complexity]['latency'] += latency
        results[complexity]['memory'] += memory
    
    for complexity in results:
        count = sum(1 for item in dataset if alp.classify_task(item['input']) == complexity)
        if count > 0:
            for metric in results[complexity]:
                results[complexity][metric] /= count
    
    return results

def run_long_test(alp, hours=24):
    start_time = time.time()
    end_time = start_time + (hours * 3600)
    performance_over_time = []
    
    while time.time() < end_time:
        dataset = create_diverse_dataset(10) 
        results = evaluate_model(alp, dataset)
        avg_latency = np.mean([results[c]['latency'] for c in results])
        performance_over_time.append(((time.time() - start_time) / 3600, avg_latency))
        time.sleep(300)  # Wait 5 minutes between evaluations
    
    return performance_over_time

def plot_results(adaptive_results, full_results, compressed_results):
    complexities = ['very_simple', 'simple', 'medium', 'complex']
    metrics = ['accuracy', 'latency', 'memory']
    
    fig, axs = plt.subplots(1, 3, figsize=(20, 5))
    
    for i, metric in enumerate(metrics):
        adaptive_values = [adaptive_results[c][metric] for c in complexities]
        full_values = [full_results[c][metric] for c in complexities]
        compressed_values = [compressed_results[c][metric] for c in complexities]
        
        x = np.arange(len(complexities))
        width = 0.25
        
        axs[i].bar(x - width, adaptive_values, width, label='Adaptive')
        axs[i].bar(x, full_values, width, label='Full Model')
        axs[i].bar(x + width, compressed_values, width, label='Compressed Model')
        
        axs[i].set_ylabel(metric.capitalize())
        axs[i].set_title(f'{metric.capitalize()} by Task Complexity')
        axs[i].set_xticks(x)
        axs[i].set_xticklabels(complexities, rotation=45)
        axs[i].legend()
    
    plt.tight_layout()
    plt.savefig('evaluation_results.png')
    plt.close()

def plot_long_test_results(performance_over_time):
    hours, latencies = zip(*performance_over_time)
    plt.figure(figsize=(10, 5))
    plt.plot(hours, latencies)
    plt.xlabel('Hours')
    plt.ylabel('Average Latency')
    plt.title('System Performance Over Time')
    plt.savefig('long_test_results.png')
    plt.close()

def main():
    alp = AdaptiveLlamaProxy()
    
    dataset = create_diverse_dataset(10)
    
    print("Evaluating Adaptive System...")
    adaptive_results = evaluate_model(alp, dataset, mode='adaptive')
    
    print("Evaluating Full Model Baseline...")
    full_results = evaluate_model(alp, dataset, mode='full')
    
    print("Evaluating Compressed Model Baseline...")
    compressed_results = evaluate_model(alp, dataset, mode='2bit')
    
    plot_results(adaptive_results, full_results, compressed_results)
    print("Comparison results plotted and saved as 'evaluation_results.png'")
    
    print("Running long-term test...")
    performance_over_time = run_long_test(alp, hours=24)
    plot_long_test_results(performance_over_time)
    print("Long-term test results plotted and saved as 'long_test_results.png'")
    
    # Print model sizes
    for model_type, model_path in alp.model_paths.items():
        model, _ = alp.model_cache(model_type)
        model_size = sum(p.nbytes for p in model.parameters().values()) / (1024 * 1024 * 1024)
        print(f"{model_type} model size: {model_size:.2f} GB")

if __name__ == "__main__":
    main()