import logging
from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, decode_token
import requests
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Import the Config class from the config module
from config import DevelopmentConfig

app = Flask(__name__)

# Select the appropriate configuration class
app.config.from_object(DevelopmentConfig)

jwt = JWTManager(app)

FASTAPI_URL = app.config['FASTAPI_URL']

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Endpoint for rendering the index.html page
@app.route('/')
def home():
    return render_template('index.html')

# Endpoint to issue JWT token based on API key
@app.route('/issue_token', methods=['POST'])
def issue_token():
    data = request.get_json()
    api_key = data.get('api_key')
    try:
        response = requests.post(f"{FASTAPI_URL}/issue_token", json={'api_key': api_key})
        response.raise_for_status()
        token = response.json().get('token')
        access_token = create_access_token(identity=token)
        return jsonify(access_token=access_token)
    except requests.RequestException as e:
        logging.error(f"Error issuing token: {e}")
        return jsonify(error='Invalid API key'), 401

# Endpoint to verify JWT token validity
@app.route('/verify_token', methods=['POST'])
def verify_token():
    data = request.get_json()
    token = data.get('token')
    try:
        decoded_token = decode_token(token)
        return jsonify(valid=True)
    except Exception as e:
        logging.error(f"Error verifying token: {e}")
        return jsonify(error='Invalid token'), 401

# Endpoint to upload and process the file
@app.route('/uploadfile', methods=['POST'])
@jwt_required()
def upload_file():
    file = request.files['file']
    extension = request.form['extension']
    token = get_jwt_identity()
    try:
        files = {'file': (file.filename, file.stream, file.content_type)}
        response = requests.post(f"{FASTAPI_URL}/uploadfile", headers={'Authorization': f'Bearer {token}'}, files=files, data={'extension': extension})
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        logging.error(f"Error uploading file: {e}")
        return jsonify(error='File upload failed'), 500

@app.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    data = request.get_json()
    question = data.get('question')
    token = get_jwt_identity()

    # Debug log
    app.logger.debug(f"Question: {question}")
    app.logger.debug(f"Token: {token}")

    try:
        # Pass the question as a query parameter
        response = requests.post(f"{FASTAPI_URL}/chatbot?question={question}", headers={'Authorization': f'Bearer {token}'})
        response.raise_for_status()

        # Debug log
        ai_response = response.json()
        app.logger.debug(f"AI Response: {ai_response}")

        return jsonify(ai_response)
    except requests.RequestException as e:
        # Log the full exception traceback
        logging.exception("Error during chat request:")

        # Return a detailed error response
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
