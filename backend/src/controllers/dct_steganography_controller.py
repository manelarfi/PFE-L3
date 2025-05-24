# src/controllers/dct_steganography_controller.py

import os
import uuid
from flask import jsonify, request, send_from_directory
from src.services.dct_steganography_service import DCTSteganographyService

# Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMP_DIR = os.path.join(PROJECT_ROOT, 'tmp')

# Create the temp directory only if it doesn't exist
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)


def dct_encode_image():
    # Validate inputs
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    if 'message' not in request.form:
        return jsonify({'error': 'No message provided'}), 400

    image_file = request.files['image']
    message = request.form['message']

    # Generate unique filename
    unique_filename = f"{uuid.uuid4().hex}.jpg"
    image_path = os.path.join(TEMP_DIR, unique_filename)

    # Save original image
    image_file.save(image_path)

    # Define output path
    stego_filename = f"stego_{unique_filename}"
    stego_path = os.path.join(TEMP_DIR, stego_filename)

    # Call service
    try:
        DCTSteganographyService.encode_dct_jpeg_like(image_path, message, stego_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'stego_image': stego_filename,
        'temp_dir': os.path.basename(TEMP_DIR)
    }), 200


def dct_decode_image():
    # Validate input
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']

    # Generate unique filename
    unique_filename = f"{uuid.uuid4().hex}.jpg"
    image_path = os.path.join(TEMP_DIR, unique_filename)

    # Save uploaded image
    image_file.save(image_path)

    # Call service
    try:
        decoded_message = DCTSteganographyService.decode_dct_jpeg_like(image_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'decoded_message': decoded_message
    }), 200


def serve_tmp_file(filename):
    """Serve files saved under tmp/ (e.g. the stego images)."""
    return send_from_directory(TEMP_DIR, filename)
