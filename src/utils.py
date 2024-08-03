import json
import random
import nltk
from nltk.corpus import wordnet

def create_diverse_dataset(size=10):
    with open('data/task_classification_data.json', 'r') as f:
        data = json.load(f)
    
    dataset = []
    complexities = list(data.keys())
    
    for _ in range(size):
        complexity = random.choice(complexities)
        base_prompt = random.choice(data[complexity])
        
        # Modify the prompt to create more diversity
        words = base_prompt.split()
        for i in range(len(words)):
            if random.random() < 0.1:  # 10% chance to replace a word
                synsets = wordnet.synsets(words[i])
                if synsets:
                    words[i] = random.choice(synsets).lemmas()[0].name()
        
        modified_prompt = ' '.join(words)
        
        dataset.append({
            'input': modified_prompt,
            'target': complexity,
            'original': base_prompt
        })
    
    return dataset

def load_classification_data(file_path='data/task_classification_data.json'):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    queries = []
    labels = []
    for complexity, prompts in data.items():
        queries.extend(prompts)
        labels.extend([complexity] * len(prompts))
    
    # Shuffle the data
    combined = list(zip(queries, labels))
    random.shuffle(combined)
    queries, labels = zip(*combined)
    
    return list(queries), list(labels)