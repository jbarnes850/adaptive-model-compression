from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report
import numpy as np
import joblib

class TaskClassifier:
    def __init__(self):
        self.vectorizer = None
        self.clf = None

    def train(self, queries, labels):
        self.vectorizer = TfidfVectorizer(max_features=200)
        X = self.vectorizer.fit_transform(queries)
        X = self.add_custom_features(X, queries)

        X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

        self.clf = RandomForestClassifier(n_estimators=100, random_state=42)
        self.clf.fit(X_train, y_train)

        accuracy = self.clf.score(X_test, y_test)
        print(f"Task classifier accuracy: {accuracy:.2f}")

        cv_scores = cross_val_score(self.clf, X, labels, cv=5)
        print(f"Cross-validation scores: {cv_scores}")
        print(f"Mean CV score: {np.mean(cv_scores):.2f}")

        y_pred = self.clf.predict(X_test)
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))

    def classify(self, prompt):
        if self.vectorizer is None or self.clf is None:
            raise ValueError("Classifier not trained. Call train() first.")

        X = self.vectorizer.transform([prompt])
        X = self.add_custom_features(X, [prompt])
        probabilities = self.clf.predict_proba(X)[0]
        
        classes = ['very_simple', 'simple', 'medium', 'complex']
        return {class_name: prob for class_name, prob in zip(classes, probabilities)}

    def classify_with_confidence(self, prompt, threshold=0.6):
        probabilities = self.classify(prompt)
        max_prob = max(probabilities.values())
        if max_prob >= threshold:
            return max(probabilities, key=probabilities.get)
        else:
            return "Uncertain"

    def update(self, new_queries, new_labels):
        X_new = self.vectorizer.transform(new_queries)
        X_new = self.add_custom_features(X_new, new_queries)
        self.clf.fit(X_new, new_labels)

    def save_model(self, filepath):
        joblib.dump(self, filepath)

    def load_model(self, filepath):
        try:
            loaded_obj = joblib.load(filepath)
            if isinstance(loaded_obj, tuple):
                # Old format: (vectorizer, clf)
                self.vectorizer, self.clf = loaded_obj
            elif isinstance(loaded_obj, TaskClassifier):
                # New format: TaskClassifier object
                self.vectorizer = loaded_obj.vectorizer
                self.clf = loaded_obj.clf
            else:
                raise ValueError("Unknown model format")
        except FileNotFoundError:
            raise FileNotFoundError(f"Model file not found at {filepath}")
        except Exception as e:
            raise Exception(f"Error loading model: {str(e)}")

    def add_custom_features(self, X, queries):
        text_lengths = np.array([len(query) for query in queries]).reshape(-1, 1)
        return np.hstack((X.toarray(), text_lengths))
