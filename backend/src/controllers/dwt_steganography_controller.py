# src/controllers/dwt_steganography_controller.py

import os
import uuid
import cv2
import numpy as np
from flask import jsonify, request, send_file, make_response
from src.services.dwt_steganography_service import DWTSteganographyService
from io import BytesIO

# Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMP_DIR     = os.path.join(PROJECT_ROOT, 'tmp')
os.makedirs(TEMP_DIR, exist_ok=True)


def _bits_to_message(bits: list[int]) -> str:
    """Pack bits back into bytes and decode UTF-8, stopping at null."""
    n = (len(bits) // 8) * 8
    arr = np.packbits(np.array(bits[:n], dtype=np.uint8))
    text = arr.tobytes().decode('utf-8', errors='ignore')
    return text.split('\0', 1)[0]  # drop after null terminator


def dwt_encode_image():
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
        image_bytes = DWTSteganographyService.encode(image_file, message, None)
        
        # Create response with image data
        response = make_response(image_bytes)
        response.headers.set('Content-Type', 'image/png')
        response.headers.set(
            'Content-Disposition', 'attachment', filename='stego_image.png'
        )
        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def dwt_decode_image():
    # Validate input
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']

    # Call service
    try:
        decoded = DWTSteganographyService.decode(image_file)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'text': decoded
    }), 200


def serve_tmp_file(filename):
    """Serve files saved under tmp/ (e.g. the stego images)."""
    return send_from_directory(TEMP_DIR, filename)
