import os
import time
import psutil
import logging
from typing import Dict, Any, Tuple
from mlx_lm import load, generate
from src.task_classifier import TaskClassifier
import concurrent.futures

class AdaptiveLlamaProxy:
    def __init__(self):
        self.logger = self.setup_logger()
        self.task_classifier = TaskClassifier()
        self.load_classifier()
        self.models: Dict[str, Tuple[Any, Any]] = {}
        self.model_paths = {
            'simple': "mlx-community/Meta-Llama-3.1-8B-Instruct-4bit",
            'medium': "mlx-community/Meta-Llama-3.1-70B-Instruct-4bit",
            'complex': "mlx-community/Meta-Llama-3.1-405B-2bit"
        }
        self.model_sizes = {
            'simple': 8,
            'medium': 70,
            'complex': 405
        }
        # Set the cache directory
        self.cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "adaptive_llama_proxy")
        os.environ['TRANSFORMERS_CACHE'] = self.cache_dir
        os.environ['HF_HOME'] = self.cache_dir

        self.model_usage = {"full": 0, "8bit": 0, "4bit": 0}
        self.total_requests = 0
        self.total_memory_saved = 0

    def load_classifier(self):
        classifier_path = os.path.join('data', 'task_classifier.joblib')
        if os.path.exists(classifier_path):
            self.task_classifier.load_model(classifier_path)
        else:
            raise FileNotFoundError(f"Classifier model not found at {classifier_path}. Please train the classifier first.")

    def setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def load_model(self, complexity: str, timeout: int = 300):
        if complexity not in self.models:
            self.logger.info(f"Loading {complexity} model...")
            if not self.check_memory(complexity):
                raise MemoryError(f"Not enough memory to load {complexity} model")
            try:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(load, self.model_paths[complexity], cache_dir=self.cache_dir)
                    model, tokenizer = future.result(timeout=timeout)
                self.models[complexity] = (model, tokenizer)
                self.logger.info(f"{complexity.capitalize()} model loaded successfully.")
            except concurrent.futures.TimeoutError:
                raise TimeoutError(f"Loading {complexity} model timed out after {timeout} seconds")
            except Exception as e:
                raise RuntimeError(f"Error loading {complexity} model: {str(e)}")
        return self.models[complexity]

    def check_memory(self, complexity: str) -> bool:
        available_memory = psutil.virtual_memory().available / (1024 ** 3)  # Available memory in GB
        required_memory = self.model_sizes[complexity] * 1.5  # Estimate 1.5x model size for safety
        return available_memory > required_memory

    def classify_task(self, prompt: str) -> str:
        classification, confidence = self.task_classifier.classify_with_confidence(prompt)
        self.logger.info(f"Task classified as {classification} with confidence {confidence:.2f}")
        return classification if classification != "Uncertain" else "medium"

    def select_model(self, task_complexity: str) -> str:
        complexity_map = {
            'very_simple': 'simple',
            'simple': 'simple',
            'medium': 'medium',
            'complex': 'complex'
        }
        return complexity_map.get(task_complexity, 'medium')

    def adaptive_generate(self, prompt: str, task_complexity: str = None) -> Dict[str, Any]:
        self.total_requests += 1
        if task_complexity is None:
            task_complexity = self.classify_task(prompt)
        
        model_type = self.select_model(task_complexity)
        try:
            model, tokenizer = self.load_model(model_type)
        except Exception as e:
            self.logger.error(f"Error loading model: {str(e)}")
            return {'error': str(e)}
        
        start_time = time.time()
        response = self.generate_response(prompt, model, tokenizer)
        generation_time = time.time() - start_time
        
        memory_usage = psutil.virtual_memory().percent
        
        # Update model usage
        if model_type == 'simple':
            self.model_usage['4bit'] += 1
        elif model_type == 'medium':
            self.model_usage['8bit'] += 1
        else:
            self.model_usage['full'] += 1
        
        # Calculate memory savings
        full_model_size = self.model_sizes['complex']
        used_model_size = self.model_sizes[model_type]
        memory_saved = full_model_size - used_model_size
        self.total_memory_saved += memory_saved
        
        self.logger.info(f"Generated response using {model_type} model. Time: {generation_time:.2f}s, Memory: {memory_usage}%")
        
        return {
            'response': response,
            'task_complexity': task_complexity,
            'model_used': model_type,
            'generation_time': generation_time,
            'memory_usage': memory_usage,
            'memory_saved': memory_saved
        }

    def get_metrics(self):
        return {
            "modelUsage": self.model_usage,
            "totalRequests": self.total_requests,
            "totalMemorySaved": self.total_memory_saved
        }

    def generate_response(self, prompt: str, model: Any, tokenizer: Any) -> str:
        response = generate(model, tokenizer, prompt=prompt, verbose=True)
        return response

    def get_memory_usage(self) -> float:
        return psutil.virtual_memory().percent

    def get_loaded_models(self) -> list:
        return list(self.models.keys())

    def unload_model(self, complexity: str):
        if complexity in self.models:
            del self.models[complexity]
            self.logger.info(f"{complexity.capitalize()} model unloaded.")

    def unload_all_models(self):
        self.models.clear()
        self.logger.info("All models unloaded.")