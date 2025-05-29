# src/controllers/dct_steganography_controller.py

import os
from flask import jsonify, request, make_response
from src.services.dct_steganography_service import DCTSteganographyService

def dct_encode_image():
    # Validate inputs
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    if 'message' not in request.form:
        return jsonify({'error': 'No message provided'}), 400

    image_file = request.files['image']
    message = request.form['message']

    # Call service
    try:
        # Get image bytes from service
        image_bytes = DCTSteganographyService.encode_dct_jpeg_like(image_file, message)
        
        # Create response with image data
        response = make_response(image_bytes)
        response.headers.set('Content-Type', 'image/png')
        response.headers.set(
            'Content-Disposition', 'attachment', filename='stego_image.png'
        )
        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def dct_decode_image():
    # Validate input
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']

    # Call service
    try:
        decoded_message = DCTSteganographyService.decode_dct_jpeg_like(image_file)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'text': decoded_message
    }), 200
