from flask import Blueprint, jsonify, request
from src.controllers.steganography_controller import encode_image, decode_image

# Create a Blueprint for steganography related routes
steganography_routes = Blueprint('steganography_routes', __name__)

# Route for encoding image with a hidden message
@steganography_routes.route('/encode', methods=['POST'])
def encode():
    return encode_image()

# Route for decoding the hidden message from an image
@steganography_routes.route('/decode', methods=['POST'])
def decode():
    return decode_image()
