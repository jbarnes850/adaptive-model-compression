"""
This file defines the TaskClassifier class, which is responsible for classifying the complexity of input tasks.

The TaskClassifier uses a combination of feature extraction and machine learning to determine the complexity of a given task.

To use this classifier:
1. Instantiate the TaskClassifier class
2. Train the classifier using the train() method with a list of queries and their corresponding labels
3. Use the classify() or classify_with_confidence() methods to classify new tasks

Example:
    classifier = TaskClassifier()
    classifier.train(queries, labels)
    complexity, confidence = classifier.classify_with_confidence("What is the capital of France?")

Note: Make sure to have the 'en_core_web_sm' spaCy model installed before using this classifier.
"""

import numpy as np
import pandas as pd
import joblib
from typing import List, Dict, Tuple, Union
import logging
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder
from xgboost import XGBClassifier

class TaskClassifier:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.pipeline = None
        self.logger = self._setup_logger()
        self.tfidf = TfidfVectorizer(max_features=1000)
        self.label_encoder = LabelEncoder()

    @staticmethod
    def _setup_logger() -> logging.Logger:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def extract_features(self, text: str) -> Dict[str, Union[int, float]]:
        doc = self.nlp(text)
        return {
            'word_count': len(doc),
            'avg_word_length': np.mean([len(token.text) for token in doc]),
            'noun_count': sum(1 for token in doc if token.pos_ == 'NOUN'),
            'verb_count': sum(1 for token in doc if token.pos_ == 'VERB'),
            'adj_count': sum(1 for token in doc if token.pos_ == 'ADJ'),
            'entity_count': len(doc.ents),
            'sentence_count': len(list(doc.sents)),
            'avg_sentence_length': np.mean([len(sent) for sent in doc.sents]) if len(list(doc.sents)) > 0 else 0,
            'unique_word_ratio': len(set(token.text.lower() for token in doc)) / len(doc) if len(doc) > 0 else 0,
        }

    def features_to_dataframe(self, features: List[Dict[str, Union[int, float]]]) -> pd.DataFrame:
        return pd.DataFrame(features)

    def train(self, queries: List[str], labels: List[str]) -> None:
        features = [self.extract_features(query) for query in queries]
        X_features = self.features_to_dataframe(features)
        X_tfidf = self.tfidf.fit_transform(queries)
        
        X = np.hstack((X_features, X_tfidf.toarray()))
        y = self.label_encoder.fit_transform(labels)
        
        # Print data distribution
        unique_labels, counts = np.unique(y, return_counts=True)
        self.logger.info("Data distribution:")
        for label, count in zip(self.label_encoder.classes_, counts):
            self.logger.info(f"{label}: {count}")
        
        self.pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('clf', XGBClassifier(n_estimators=100, random_state=42))
        ])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.pipeline.fit(X_train, y_train)

        accuracy = self.pipeline.score(X_test, y_test)
        self.logger.info(f"Task classifier accuracy: {accuracy:.2f}")

        cv_scores = cross_val_score(self.pipeline, X, y, cv=5)
        self.logger.info(f"Cross-validation scores: {cv_scores}")
        self.logger.info(f"Mean CV score: {np.mean(cv_scores):.2f}")

        y_pred = self.pipeline.predict(X_test)
        self.logger.info("\nClassification Report:")
        self.logger.info(classification_report(y_test, y_pred, target_names=self.label_encoder.classes_))

    def classify(self, prompt: str) -> Dict[str, float]:
        if self.pipeline is None:
            raise ValueError("Classifier not trained. Call train() first.")

        features = [self.extract_features(prompt)]
        X_features = self.features_to_dataframe(features)
        X_tfidf = self.tfidf.transform([prompt])
        X = np.hstack((X_features, X_tfidf.toarray()))
        probabilities = self.pipeline.predict_proba(X)[0]
        
        return {class_name: prob for class_name, prob in zip(self.label_encoder.classes_, probabilities)}

    def classify_with_confidence(self, prompt: str) -> Tuple[str, float]:
        probabilities = self.classify(prompt)
        max_class = max(probabilities, key=probabilities.get)
        return max_class, probabilities[max_class]

    def save_model(self, path: str) -> None:
        joblib.dump((self.pipeline, self.tfidf, self.label_encoder), path)

    def load_model(self, path: str) -> None:
        self.pipeline, self.tfidf, self.label_encoder = joblib.load(path)