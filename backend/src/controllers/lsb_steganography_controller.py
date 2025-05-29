from flask import jsonify, request, make_response
from src.services.lsb_steganography_service import LSBSteganographyService
import os

def get_temp_dir():
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TEMP_DIR = os.path.join(PROJECT_ROOT, 'tmp')
    os.makedirs(TEMP_DIR, exist_ok=True)
    return TEMP_DIR

def encode_image():
    # Validate inputs
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    if 'message' not in request.form:
        return jsonify({'error': 'No message provided'}), 400

    try:
        # Get image bytes from service
        image_bytes = LSBSteganographyService.encode(
            image_file=request.files['image'],
            message=request.form['message']
        )
        
        # Create response with image data
        response = make_response(image_bytes)
        response.headers.set('Content-Type', 'image/png')
        response.headers.set(
            'Content-Disposition', 'attachment', filename='stego_image.png'
        )
        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 400

def decode_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    try:
        decoded_message = LSBSteganographyService.decode(
            image_file=request.files['image']
        )
        return jsonify({
            'text': decoded_message
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400