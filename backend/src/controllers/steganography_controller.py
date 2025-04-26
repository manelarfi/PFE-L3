from flask import jsonify, request
from src.services.steganography_service import SteganographyService

# Function to encode the image with a message
def encode_image():
    image_file = request.files['image']  # Get the image from the request
    message = request.form['message']    # Get the message from the request
    
    # Call the Steganography service to encode the image
    try:
        encoded_image = SteganographyService.encode(image_file, message)
        return jsonify({'encoded_image': encoded_image}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Function to decode a message from the image
def decode_image():
    image_file = request.files['image']  # Get the image from the request
    
    # Call the Steganography service to decode the message
    try:
        decoded_message = SteganographyService.decode(image_file)
        return jsonify({'decoded_message': decoded_message}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
