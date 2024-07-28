import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import pickle

# Load the data
data = pd.read_csv('water_leak_dataset_final.csv')

# Select features and target
X = data[['Pressure', 'Flow']]
y = data['Anomaly']

# Encode and scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply SMOTE to balance the classes
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_scaled, y)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Create and train the SVM model
model = SVC(kernel='rbf', gamma='auto', probability=True)
model.fit(X_train, y_train)

# Save the trained model and scaler
with open('svm_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

with open('scaler.pkl', 'wb') as scaler_file:
    pickle.dump(scaler, scaler_file)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy * 100, "%")
print("Classification Report:\n", classification_report(y_test, y_pred, zero_division=0))

# Function to make predictions with new input
def predict_anomaly(pressure, flow):
    # Load the model and scaler
    with open('svm_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
    
    # Prepare the data for prediction
    input_data = pd.DataFrame([[pressure, flow]], columns=['Pressure', 'Flow'])
    input_scaled = scaler.transform(input_data)
    
    # Predict using the trained model
    prediction = model.predict(input_scaled)
    
    return int(prediction[0])

# Test the function with sample inputs
pressure_input = 23.23
flow_input = 171.82
anomaly_prediction = predict_anomaly(pressure_input, flow_input)
print(f"Anomaly prediction for Pressure={pressure_input} and Flow={flow_input}: {anomaly_prediction}")