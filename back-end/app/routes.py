import shutil
from flask import Blueprint, jsonify, request, current_app, send_from_directory, abort
from functools import wraps
import jwt
import datetime
import os


# from bson.objectid import ObjectId
# from app import mongo
import app.models.user as user_model
import app.utile as utile
import bcrypt

import pickle
bp = Blueprint('api', __name__) 




def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace('Bearer ', '')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = user_model.get_All_by_email(data['email'])
            if not current_user:
                return jsonify({'message': 'User not found!'}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user['accountType'] not in ['admin', 'owner']:
            return jsonify({'message': 'Admin access required!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated


def owner_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user['accountType'] != 'owner':
            return jsonify({'message': 'Owner access required!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated


# User routes

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    required_fields = ['username', 'email', 'password']
    missing_fields = [
        field for field in required_fields if field not in data or not data[field]]

    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

    email = str(data['email']).strip().lower()
    password = str(data['password']).strip()
    username = str(data['username']).strip()

    if not utile.validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
    if not password:
        return jsonify({'error': 'Invalid password format'}), 400

    if user_model.get_user_by_email(email):
        return jsonify({'error': 'User already exists'}), 400

    if user_model.get_user_by_username(username):
        return jsonify({'error': 'User already exists'}), 400

    result = user_model.add_user(username, email, password)

    return jsonify({'message': 'User registered successfully'}), 201


@bp.route('/registerAdmin', methods=['POST'])
@token_required
@owner_required
def register_Admin(current_user):
    data = request.get_json() or {}
    required_fields = ['username', 'email', 'password']
    missing_fields = [
        field for field in required_fields if field not in data or not data[field]]

    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

    email = str(data['email']).strip().lower()
    password = str(data['password']).strip()
    username = str(data['username']).strip()

    if not utile.validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400

    if not utile.validate_password(password):
        return jsonify({'error': 'Invalid password format'}), 400

    if user_model.get_admin_by_email(email):
        return jsonify({'error': 'Admin already exists'}), 400

    if user_model.get_admin_by_username(username):
        return jsonify({'error': 'Admin already exists'}), 400

    result = user_model.add_admin(username, email, password)

    return jsonify({'message': 'Admin registered successfully'}), 201


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    required_fields = ['email', 'password']
    missing_fields = [
        field for field in required_fields if field not in data or not data[field]]

    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

    email = str(data.get('email')).strip().lower()
    password = str(data.get('password')).strip()

    user = user_model.get_All_by_email(email)
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = utile.generate_token(email)
    username = user["username"]
    profileImg = user["profileImg"]
    return jsonify({'message': "User login successfully", 'token': token, 'username': username, 'profileImg': profileImg})


@bp.route('/dropUser', methods=['DELETE'])
@token_required
@admin_required
def drop_user(current_user):
    data = request.get_json() or {}
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required to drop a user'}), 400

    user = user_model.get_user_by_email(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_model.delete_user(email)
    return jsonify({'message': 'User deleted successfully'}), 200


@bp.route('/dropAdmin', methods=['DELETE'])
@token_required
@owner_required
def drop_admin(current_user):
    data = request.get_json() or {}
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required to drop an admin'}), 400

    admin = user_model.get_admin_by_email(email)
    if not admin:
        return jsonify({'error': 'Admin not found'}), 404

    user_model.delete_admin(email)
    return jsonify({'message': 'Admin deleted successfully'}), 200


@bp.route('/getUsers', methods=['GET'])
@token_required
@admin_required
def get_users(current_user):
    users = user_model.get_users()
    return jsonify(users), 200


@bp.route('/getAdmins', methods=['GET'])
@token_required
@owner_required
def get_admins(current_user):
    users_and_admins = user_model.get_admins()
    return jsonify(users_and_admins), 200


@bp.route('/getUsersAndAdmins', methods=['GET'])
@token_required
@owner_required
def get_users_and_admins(current_user):
    users_and_admins = user_model.get_users_and_admins()
    return jsonify(users_and_admins), 200


@bp.route('/userRole', methods=['GET'])
@token_required
def get_user_role(current_user):
    user_role = current_user.get('accountType')
    if not user_role:
        return jsonify({"error": "invalid user type"})
    return jsonify({"role": user_role}), 200


import pandas as pd



import joblib

# # Function to load model and encoder
# def load_model_and_encoder():
#     model = joblib.load('./logistic_regression_model.joblib')
#     encoder = joblib.load('./encoder.joblib')
#     return model, encoder

# # Function to predict with the model
# def predict(model, encoder, input_data):
#     input_encoded = encoder.transform(input_data)
#     prediction = model.predict(input_encoded)
#     return prediction


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


@bp.route('/predict', methods=['POST'])
@token_required
def predict_data(current_user):
    data = request.get_json()
    pressure = data['pressure']
    flow = data['flow']

    # Access the model and encoder from the app config
    # Load the trained model and encoder with joblib
    # model = current_app.config['MODEL']
    # encoder=current_app.config['ENCODER']

    prediction = predict_anomaly(pressure, flow)


    # Return the prediction as a JSON response
    return jsonify({'anomaly': int(prediction)})
