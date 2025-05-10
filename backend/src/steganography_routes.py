from flask import Blueprint
from src.controllers.lsb_steganography_controller import encode_image, decode_image

from src.controllers.dwt_steganography_controller import dwt_encode_image, dwt_decode_image

steganography_bp = Blueprint('steganography', __name__, url_prefix='/api/steganography')

# LSB Routes
@steganography_bp.route('/lsb/encode', methods=['POST'])
def lsb_encode():
    return encode_image()

@steganography_bp.route('/lsb/decode', methods=['POST'])
def lsb_decode():
    return decode_image()

# DWT Routes
@steganography_bp.route('/dwt/encode', methods=['POST'])
def dwt_encode():
    return dwt_encode_image()

@steganography_bp.route('/dwt/decode', methods=['POST'])
def dwt_decode():
    return dwt_decode_image()