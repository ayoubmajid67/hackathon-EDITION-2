import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import OneHotEncoder
import pickle
from flask import Flask, request, jsonify

# Load the data
data = pd.read_csv('water_leak_dataset_final.csv')

# Select features and target
X = data[['Pressure', 'Flow']]
y = data['Anomaly']

# Encode features
encoder = OneHotEncoder()
X_encoded = encoder.fit_transform(X)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# Create and train the model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save the trained model and encoder
with open('logistic_regression_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

with open('encoder.pkl', 'wb') as encoder_file:
    pickle.dump(encoder, encoder_file)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy * 100, "%")
print("Classification Report:\n", classification_report(y_test, y_pred, zero_division=0))

# Flask application
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    pressure = data['pressure']
    flow = data['flow']

    # Prepare the data for prediction
    input_data = pd.DataFrame([[pressure, flow]], columns=['Pressure', 'Flow'])
    input_encoded = encoder.transform(input_data)

    # Predict using the trained model
    prediction = model.predict(input_encoded)

    # Return the prediction as a JSON response
    return jsonify({'anomaly': int(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True)
