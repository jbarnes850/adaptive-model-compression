import os
import psutil
import logging
import time
from mlx_lm import load, generate
from functools import lru_cache
import gc
from src.task_classifier import TaskClassifier

class AdaptiveLlamaProxy:
    def __init__(self, max_memory_usage=90, model_cache_size=2):
        self.models = {}
        self.tokenizers = {}
        self.logger = self.setup_logger()
        self.max_memory_usage = max_memory_usage
        self.model_paths = {
            '2bit': "mlx-community/Meta-Llama-3-8B-Instruct-4bit",
            'full': "mlx-community/Meta-Llama-3.1-8B-bf16",
            '4bit': "mlx-community/Meta-Llama-3.1-70B-Instruct-4bit",
            '8bit': "mlx-community/Meta-Llama-3.1-70B-Instruct-8bit"
        }
        self.model_cache = lru_cache(maxsize=model_cache_size)(self._load_model)

    def setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _load_model(self, model_type):
        if model_type not in self.model_paths:
            raise ValueError(f"Unknown model type: {model_type}")
        
        path = self.model_paths[model_type]
        self.logger.info(f"Loading {model_type} model...")
        
        available_memory = psutil.virtual_memory().available / (1024 * 1024 * 1024)  # in GB
        self.logger.info(f"Available memory before loading: {available_memory:.2f} GB")
        
        if psutil.virtual_memory().percent > self.max_memory_usage:
            self.unload_least_used_model()
        
        try:
            model, tokenizer = load(path)
            self.models[model_type] = model
            self.tokenizers[model_type] = tokenizer
            self.logger.info(f"{model_type.capitalize()} model loaded successfully")
            return model, tokenizer
        except Exception as e:
            self.logger.error(f"Failed to load {model_type} model: {str(e)}")
            raise

    def classify_task(self, prompt):
        if not hasattr(self, 'task_classifier'):
            self.task_classifier = TaskClassifier()
            current_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(current_dir, '..', 'data', 'task_classifier.joblib')
            self.task_classifier.load_model(model_path)
    
        classification = self.task_classifier.classify_with_confidence(prompt)
        return classification if classification != "Uncertain" else "medium"

    def select_model(self, task_complexity):
        complexity_map = {
            'very_simple': '2bit',
            'simple': 'full',
            'medium': '4bit',
            'complex': '8bit'
        }
        return complexity_map.get(task_complexity, 'full')

    def adaptive_generate(self, prompt, task_complexity=None):
        if task_complexity is None:
            task_complexity = self.classify_task(prompt)
        
        model_type = self.select_model(task_complexity)
        model, tokenizer = self.model_cache(model_type)
        
        start_time = time.time()
        response = generate(model, tokenizer, prompt=prompt, verbose=True)
        generation_time = time.time() - start_time
        
        memory_usage = psutil.virtual_memory().percent
        
        self.logger.info(f"Generated response using {model_type} model. Time: {generation_time:.2f}s, Memory: {memory_usage}%")
        
        return {
            'response': response,
            'task_complexity': task_complexity,
            'model_used': model_type,
            'generation_time': generation_time,
            'memory_usage': memory_usage
        }

    def get_memory_usage(self):
        return psutil.virtual_memory().percent

    def unload_least_used_model(self):
        if self.models:
            least_used = min(self.models, key=lambda k: self.model_cache.cache_info().hits)
            self.unload_model(least_used)

    def unload_model(self, model_type):
        if model_type in self.models:
            del self.models[model_type]
            del self.tokenizers[model_type]
            self.model_cache.cache_clear()
            gc.collect()
            self.logger.info(f"Unloaded {model_type} model")

    def unload_all_models(self):
        self.models.clear()
        self.tokenizers.clear()
        self.model_cache.cache_clear()
        gc.collect()
        self.logger.info("All models unloaded")

    def get_loaded_models(self):
        return list(self.models.keys())