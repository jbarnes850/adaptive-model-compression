import sys
import os
import joblib
import json
from sklearn.model_selection import train_test_split
import threading
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.task_classifier import TaskClassifier

CLASSIFIER_PATH = os.path.join('data', 'task_classifier.joblib')
DATA_PATH = os.path.join('data', 'task_classification_data.json')
UPDATE_THRESHOLD = 1000  # Number of new samples before updating
UPDATE_INTERVAL = 86400  # Time in seconds between updates (e.g., 24 hours)

class ClassifierManager:
    def __init__(self):
        self.classifier = self.load_or_create_classifier()
        self.new_data = []
        self.lock = threading.Lock()
        self.last_update_time = time.time()

    def load_or_create_classifier(self):
        if os.path.exists(CLASSIFIER_PATH):
            print("Loading existing classifier...")
            classifier = TaskClassifier()
            try:
                classifier.load_model(CLASSIFIER_PATH)
            except Exception as e:
                print(f"Error loading existing classifier: {str(e)}")
                print("Creating new classifier...")
                queries, labels = self.load_classification_data()
                classifier.train(queries, labels)
                classifier.save_model(CLASSIFIER_PATH)
            return classifier
        else:
            print("Creating new classifier...")
            classifier = TaskClassifier()
            queries, labels = self.load_classification_data()
            classifier.train(queries, labels)
            classifier.save_model(CLASSIFIER_PATH)
            return classifier

    def load_classification_data(self):
        with open(DATA_PATH, 'r') as f:
            data = json.load(f)
        
        queries = []
        labels = []
        for complexity, examples in data.items():
            queries.extend(examples)
            labels.extend([complexity] * len(examples))
        
        return queries, labels

    def classify(self, query):
        with self.lock:
            return self.classifier.classify(query)

    def add_new_data(self, query, label):
        self.new_data.append((query, label))

    def update_classifier(self):
        if len(self.new_data) >= UPDATE_THRESHOLD and time.time() - self.last_update_time >= UPDATE_INTERVAL:
            print("Updating classifier...")
            new_queries, new_labels = zip(*self.new_data)
            
            # Load all historical data
            historical_queries, historical_labels = self.load_classification_data()
            
            # Combine historical and new data
            all_queries = historical_queries + list(new_queries)
            all_labels = historical_labels + list(new_labels)
            
            # Train the classifier on all data
            self.classifier.train(all_queries, all_labels)
            
            self.new_data.clear()
            self.last_update_time = time.time()
            
            # Save the updated classifier
            self.classifier.save_model(CLASSIFIER_PATH)
            print("Classifier updated and saved.")

def background_updater(manager):
    while True:
        time.sleep(UPDATE_INTERVAL)
        manager.update_classifier()

def main():
    manager = ClassifierManager()
    
    # Start background updater thread
    updater_thread = threading.Thread(target=background_updater, args=(manager,), daemon=True)
    updater_thread.start()

    # Example usage
    print("Classifying a sample query...")
    sample_query = "What is the capital of France?"
    classification = manager.classify(sample_query)
    print(f"Classification: {classification}")

    # Keep the main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()