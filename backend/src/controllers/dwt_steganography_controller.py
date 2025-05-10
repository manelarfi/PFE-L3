# src/controllers/dwt_steganography_controller.py
from flask import jsonify, request
from src.services.dwt_steganography_service import DWTSteganographyService
import os

# Get the project root directory (where your Flask app resides)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMP_DIR = os.path.join(PROJECT_ROOT, 'tmp')

# Ensure the temp directory exists
os.makedirs(TEMP_DIR, exist_ok=True)

def dwt_encode_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    if 'message' not in request.form:
        return jsonify({'error': 'No message provided'}), 400

    image_file = request.files['image']
    message = request.form['message']
    
    try:
        encoded_image = DWTSteganographyService.encode(
            image_file=image_file,
            message=message,
            temp_dir=TEMP_DIR
        )
        return jsonify({
            'encoded_image': encoded_image,
            'algorithm': 'DWT',
            'temp_dir': TEMP_DIR  # Optional: for debugging
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def dwt_decode_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    
    try:
        decoded_message = DWTSteganographyService.decode(
            image_file=image_file,
            temp_dir=TEMP_DIR
        )
        return jsonify({
            'decoded_message': decoded_message,
            'algorithm': 'DWT'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400