# # src/controllers/dwt_steganography_controller.py
# import io
# import os
# import uuid
# import cv2
# import numpy as np
# from flask import jsonify, request, send_from_directory
# from src.services.dwt_steganography_service import DWTSteganographyService

# # Paths
# PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# TEMP_DIR     = os.path.join(PROJECT_ROOT, 'tmp')
# os.makedirs(TEMP_DIR, exist_ok=True)

# def _message_to_bits(msg: str) -> np.ndarray:
#     data = msg.encode('utf-8')
#     bits = np.unpackbits(np.frombuffer(data, dtype=np.uint8))
#     return bits.tolist()

# def _bits_to_message(bits: list[int]) -> str:
#     # Trim to nearest byte
#     n = (len(bits) // 8) * 8
#     arr = np.packbits(np.array(bits[:n], dtype=np.uint8))
#     return arr.tobytes().decode('utf-8', errors='ignore')

# def dwt_encode_image():
#     if 'image' not in request.files:
#         return jsonify({'error': 'No image uploaded'}), 400
#     if 'message' not in request.form:
#         return jsonify({'error': 'No message provided'}), 400

#     # Read upload
#     file = request.files['image']
#     in_mem = np.frombuffer(file.read(), np.uint8)
#     cover = cv2.imdecode(in_mem, cv2.IMREAD_GRAYSCALE)
#     if cover is None:
#         return jsonify({'error': 'Invalid image file'}), 400

#     # Convert message to bitstream
#     bitstream = _message_to_bits(request.form['message'])

#     # Embed
#     stego_img, key_matrix = DWTSteganographyService.encode(cover, bitstream)

#     # Save results with unique names
#     uid        = uuid.uuid4().hex
#     stego_name = f'stego_{uid}.png'
#     key_name   = f'key_{uid}.npy'
#     stego_path = os.path.join(TEMP_DIR, stego_name)
#     key_path   = os.path.join(TEMP_DIR, key_name)

#     cv2.imwrite(stego_path, stego_img)
#     np.save(key_path, key_matrix)

#     return jsonify({
#         'stego_image': stego_name,
#         'key_file'  : key_name
#     }), 200

# def dwt_decode_image():
#     if 'image' not in request.files or 'key' not in request.files:
#         return jsonify({'error': 'Image and key matrix required'}), 400

#     # Load stego image
#     img_file = request.files['image']
#     in_mem   = np.frombuffer(img_file.read(), np.uint8)
#     stego    = cv2.imdecode(in_mem, cv2.IMREAD_GRAYSCALE)
#     if stego is None:
#         return jsonify({'error': 'Invalid stego image'}), 400

#     # Load key matrix
#     key_file = request.files['key']
#     key_buf  = key_file.read()
#     try:
#         key_matrix = np.load(io.BytesIO(key_buf))
#     except Exception:
#         return jsonify({'error': 'Invalid key matrix'}), 400

#     # Extract bitstream
#     bits = DWTSteganographyService.decode(stego, key_matrix)
#     message = _bits_to_message(bits)

#     return jsonify({
#         'decoded_message': message
#     }), 200

# # Optional endpoints to serve the generated files
# def serve_tmp_file(filename):
#     return send_from_directory(TEMP_DIR, filename)
