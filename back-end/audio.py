import librosa
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

class SelfLearningAudioClassifier:
    def _init_(self, n_mfcc=13, max_len=100):
        self.n_mfcc = n_mfcc
        self.max_len = max_len
        self.model = SVC(probability=True)
        self.scaler = StandardScaler()
        self.data = []
        self.labels = []
        self.trained = False
        
    def extract_mfcc(self, y, sr):
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=self.n_mfcc)
        if mfcc.shape[1] < self.max_len:
            pad_width = self.max_len - mfcc.shape[1]
            mfcc = np.pad(mfcc, ((0, 0), (0, pad_width)), mode='constant')
        else:
            mfcc = mfcc[:, :self.max_len]
        return mfcc.flatten()

    def fit(self, files, labels):
        for file, label in zip(files, labels):
            y, sr = librosa.load(file, duration=5)
            features = self.extract_mfcc(y, sr)
            self.data.append(features)
            self.labels.append(label)
        
        X = np.array(self.data)
        y = np.array(self.labels)
        
        # Standardize features
        X = self.scaler.fit_transform(X)
        
        # Train initial model
        self.model.fit(X, y)
        self.trained = True

    def predict(self, file):
        if not self.trained:
            raise ValueError("Model is not trained yet.")
        
        y, sr = librosa.load(file, duration=5)
        features = self.extract_mfcc(y, sr)
        features = self.scaler.transform([features])
        return self.model.predict(features)
    
    def add_new_data(self, file, label):
        y, sr = librosa.load(file, duration=5)
        features = self.extract_mfcc(y, sr)
        self.data.append(features)
        self.labels.append(label)
        
        # Retrain model with new data
        X = np.array(self.data)
        y = np.array(self.labels)
        X = self.scaler.fit_transform(X)
        self.model.fit(X, y)
        self.trained = True
    
    def calculate_similarity(self, file1, file2):
        y1, sr1 = librosa.load(file1, duration=5)
        features1 = self.extract_mfcc(y1, sr1)
        y2, sr2 = librosa.load(file2, duration=5)
        features2 = self.extract_mfcc(y2, sr2)
        
        return cosine_similarity([features1], [features2])[0][0]

# Initial setup with provided files
files = ['fuite.wav', 'goutte.wav']
labels = [1, 0]

classifier = SelfLearningAudioClassifier()
classifier.fit(files, labels)

# Example of adding new data
# classifier.add_new_data('new_audio.wav', 1) # Assuming 'new_audio.wav' has label 1

# Example of prediction
# print(classifier.predict('some_audio.wav'))

# Example of calculating similarity
# similarity = classifier.calculate_similarity('fuite.wav', 'goutte.wav')
# print(f"Cosine Similarity: {similarity}")

# Save the classifier and scaler for later use
import joblib
joblib.dump(classifier, 'self_learning_audio_classifier.pkl')