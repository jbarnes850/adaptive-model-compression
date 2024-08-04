import sys
import os
from datasets import load_dataset, concatenate_datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.task_classifier import TaskClassifier

CLASSIFIER_PATH = os.path.join('data', 'task_classifier.joblib')

def load_mmlu_data():
    ds = load_dataset("cais/mmlu", "all")
    
    # Combine all available splits
    all_data = concatenate_datasets([ds[split] for split in ds.keys() if split != 'auxiliary_train'])
    
    # Convert to pandas DataFrame
    df = all_data.to_pandas()
    
    # Print subject information
    print("Subject information:")
    print(df['subject'].value_counts())
    
    # Print a few sample questions from each subject
    for subject in df['subject'].unique():
        print(f"\nSample questions from {subject}:")
        print(df[df['subject'] == subject]['question'].head(3))
    
    # Map subject difficulty to our complexity levels
    difficulty_mapping = {
        'elementary': 'simple',
        'high_school': 'medium',
        'college': 'complex',
        'professional': 'complex'
    }
    
    df['complexity'] = df['subject'].map(lambda x: difficulty_mapping.get(x.split('_')[0], 'medium'))
    
    print("\nDataset information:")
    print(df['subject'].value_counts())
    
    print("\nComplexity distribution:")
    print(df['complexity'].value_counts())
    
    return df['question'].tolist(), df['complexity'].tolist()

def train_classifier():
    print("Loading MMLU data...")
    queries, labels = load_mmlu_data()

    print(f"\nTotal samples: {len(queries)}")

    classifier = TaskClassifier()
    classifier.train(queries, labels)

    print("Saving classifier...")
    classifier.save_model(CLASSIFIER_PATH)
    print(f"Classifier saved to {CLASSIFIER_PATH}")

    return classifier

def main():
    classifier = train_classifier()

    print("\nClassifying sample queries...")
    sample_queries = [
        "What's the color of the sky?",
        "How many days are in a week?",
        "What's the capital of France?",
        "How do I make a sandwich?",
        "Explain the basics of photosynthesis",
        "How does a combustion engine work?",
        "Analyze the economic impact of climate change",
        "Discuss the philosophical implications of artificial intelligence",
        "What are the main causes of climate change?",
        "Explain the concept of supply and demand in economics",
        "How does quantum computing differ from classical computing?",
        "Describe the process of evolution",
        "What are the implications of blockchain technology?",
        "How does the human brain process information?"
    ]

    for query in sample_queries:
        classification, confidence = classifier.classify_with_confidence(query)
        print(f"Query: '{query}'")
        print(f"Classification: {classification}")
        print(f"Confidence: {confidence:.2f}\n")

if __name__ == "__main__":
    main()