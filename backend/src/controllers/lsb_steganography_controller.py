from flask import jsonify, request
from src.services.lsb_steganography_service import LSBSteganographyService
import os

def get_temp_dir():
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TEMP_DIR = os.path.join(PROJECT_ROOT, 'tmp')
    os.makedirs(TEMP_DIR, exist_ok=True)
    return TEMP_DIR

def encode_image():  # Changed from lsb_encode_image
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    if 'message' not in request.form:
        return jsonify({'error': 'No message provided'}), 400

    try:
        encoded_image = LSBSteganographyService.encode(
            image_file=request.files['image'],
            message=request.form['message'],
            temp_dir=get_temp_dir()
        )
        return jsonify({
            'encoded_image': encoded_image,
            'algorithm': 'LSB'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def decode_image():  # Changed from lsb_decode_image
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    try:
        decoded_message = LSBSteganographyService.decode(
            image_file=request.files['image'],
            temp_dir=get_temp_dir()
        )
        return jsonify({
            'decoded_message': decoded_message,
            'algorithm': 'LSB'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400