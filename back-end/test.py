import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import OneHotEncoder
import os
import joblib

# Function to load data
def load_data(csv_file_path):
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"{csv_file_path} not found. Please check the path.")
    return pd.read_csv(csv_file_path)

# Function to encode features
def encode_features(X):
    encoder = OneHotEncoder(handle_unknown='ignore')
    X_encoded = encoder.fit_transform(X)
    return X_encoded, encoder

# Function to train and save the model
def train_and_save_model(X_train, y_train):
    model = LogisticRegression()
    model.fit(X_train, y_train)
    joblib.dump(model, 'logistic_regression_model.joblib')
    return model

# Function to evaluate the model
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy * 100, "%")
    print("Classification Report:\n", classification_report(y_test, y_pred, zero_division=0))
    return accuracy

# Function to load model and encoder
def load_model_and_encoder():
    model = joblib.load('logistic_regression_model.joblib')
    encoder = joblib.load('encoder.joblib')
    return model, encoder

# Function to predict with the model
def predict(model, encoder, input_data):
    input_encoded = encoder.transform(input_data)
    prediction = model.predict(input_encoded)
    return prediction

# Main function to execute the workflow
def main():
    # Load the data
    data = load_data('water_leak_dataset_final.csv')

    # Select features and target
    X = data[['Pressure', 'Flow']]
    y = data['Anomaly']

    # Encode features with handling unknown categories
    X_encoded, encoder = encode_features(X)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

    # Create and train the model
    model = train_and_save_model(X_train, y_train)

    # Save the encoder
    joblib.dump(encoder, 'encoder.joblib')

    # Evaluate the model
    evaluate_model(model, X_test, y_test)

    # Load the trained model and encoder
    model, encoder = load_model_and_encoder()

    # Prepare input data
    input_data = pd.DataFrame([[40, 130]], columns=['Pressure', 'Flow'])

    # Predict using the trained model
    prediction = predict(model, encoder, input_data)
    print(prediction[0])

if __name__ == "__main__":
    main()
