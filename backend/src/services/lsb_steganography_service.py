import cv2
import numpy as np
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure temp directory (relative to project root)
app.config['TEMP_DIR'] = os.path.join(app.root_path, 'tmp')

# Create temp directory if it doesn't exist
os.makedirs(app.config['TEMP_DIR'], exist_ok=True)

class LSBSteganographyService:
    
    @staticmethod
    def calculate_capacity(image_shape, lsb_count=1):
        """Calculate the maximum message length that can be embedded"""
        height, width, channels = image_shape
        total_pixels = height * width
        total_bits = total_pixels * channels * lsb_count
        # Remove 24 bits (3 bytes) for storing metadata in last pixel
        total_bits -= 24
        # Each character needs 8 bits, and we need 5 bytes for delimiter
        return (total_bits // 8) - 5  # 5 bytes for '#####' delimiter

    @staticmethod
    def encode(image_file, message: str) -> bytes:
        """Encodes a message into an image using dynamic LSB count and returns image bytes"""
        try:
            # Read image from file object
            data = np.frombuffer(image_file.read(), np.uint8)
            img = cv2.imdecode(data, cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError("Invalid image file")

            # Add delimiter to message
            message += '#####'
            message_length = len(message)
            
            # Try different LSB counts to find minimum required
            lsb_count = None
            for bits in range(1, 5):  # Try 1 to 4 LSBs
                capacity = LSBSteganographyService.calculate_capacity(img.shape, bits)
                if message_length <= capacity:
                    lsb_count = bits
                    break
            
            if lsb_count is None:
                raise ValueError(f"Message too large for image (length: {message_length}, max capacity with 4 LSBs: {LSBSteganographyService.calculate_capacity(img.shape, 4)} characters)")

            # Convert message to binary
            binary_msg = ''.join(format(ord(c), '08b') for c in message)
            total_bits = len(binary_msg)

            # Create LSB mask and clear mask based on LSB count
            lsb_mask = (1 << lsb_count) - 1
            clear_mask = ~lsb_mask & 0xFF

            # Embed message
            flat_img = img.reshape(-1)
            data_idx = 0
            bits_per_pixel = lsb_count
            
            for i in range(0, len(flat_img) - 3):  # Leave last pixel for metadata
                if data_idx >= total_bits:
                    break
                    
                # Take next bits_per_pixel bits from message
                remaining_bits = total_bits - data_idx
                if remaining_bits < bits_per_pixel:
                    bits_per_pixel = remaining_bits
                    
                msg_bits = int(binary_msg[data_idx:data_idx + bits_per_pixel], 2)
                
                # Clear the LSBs and embed new bits
                pixel_value = flat_img[i]
                pixel_value = (pixel_value & clear_mask) | msg_bits
                flat_img[i] = pixel_value
                
                data_idx += bits_per_pixel

            # Store LSB count in last pixel
            flat_img[-3:] = [lsb_count, 0, 0]

            # Convert to bytes
            success, buffer = cv2.imencode('.png', img)
            if not success:
                raise IOError("Failed to encode image")
            
            return buffer.tobytes()
            
        except Exception as e:
            raise e

    @staticmethod
    def decode(image_file) -> str:
        """Decodes a message from an image using stored LSB count"""
        try:
            # Read image from file object
            data = np.frombuffer(image_file.read(), np.uint8)
            img = cv2.imdecode(data, cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError("Invalid image file")

            # Get LSB count from last pixel
            lsb_count = img.reshape(-1)[-3]
            if not 1 <= lsb_count <= 4:
                raise ValueError("Invalid LSB count detected")

            # Create mask for extracting LSBs
            lsb_mask = (1 << lsb_count) - 1

            # Extract bits using the LSB count
            flat_img = img.reshape(-1)[:-3]  # Exclude last pixel
            binary_msg = []
            current_byte = 0
            bits_collected = 0
            
            for pixel_value in flat_img:
                extracted_bits = pixel_value & lsb_mask
                current_byte = (current_byte << lsb_count) | extracted_bits
                bits_collected += lsb_count
                
                if bits_collected >= 8:
                    # We have a complete byte
                    binary_msg.append(chr(current_byte & 0xFF))
                    current_byte = current_byte >> 8
                    bits_collected -= 8
                    
                    # Check for delimiter
                    decoded_text = ''.join(binary_msg)
                    if '#####' in decoded_text:
                        decoded_text = decoded_text.split('#####')[0]
                        return decoded_text

            raise ValueError("No valid message found (missing delimiter)")
            
        except Exception as e:
            raise e

# Auto-cleanup on server shutdown
import atexit
@atexit.register
def cleanup():
    temp_dir = app.config['TEMP_DIR']
    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Cleanup failed for {file_path}: {e}")

# Routes
@app.route('/encode', methods=['POST'])
def handle_encode():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
        
    try:
        encoded_bytes = LSBSteganographyService.encode(
            image_file=request.files['image'],
            message=request.form.get('message', '')
        )
        return jsonify({"encoded_image": encoded_bytes})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/decode', methods=['POST'])
def handle_decode():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
        
    try:
        message = LSBSteganographyService.decode(
            image_file=request.files['image']
        )
        return jsonify({"decoded_message": message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)