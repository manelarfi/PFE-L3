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
    def calculate_required_lsb_count(message_length, image_size):
        """Calculate how many LSBs are needed per channel to store the message"""
        total_message_bits = message_length * 8  # 8 bits per character
        available_pixels = image_size // 3  # Total pixels (each has 3 channels)
        
        # Calculate required LSBs per channel
        for lsb_count in range(1, 5):  # Try 1 to 4 LSBs
            total_capacity = available_pixels * 3 * lsb_count  # Total bits we can store
            if total_capacity >= total_message_bits:
                return lsb_count
        return None  # If even 4 LSBs aren't enough
    
    @staticmethod
    def encode(image_file, message, temp_dir):
        """Encodes a message into an image using dynamic LSB count"""
        try:
            # Save uploaded file to project temp dir
            upload_path = os.path.join(temp_dir, "uploaded_" + image_file.filename)
            image_file.save(upload_path)

            # Read image
            img = cv2.imread(upload_path)
            if img is None:
                raise ValueError("Invalid image file")

            # Prepare message
            message += '#####'  # Delimiter
            message_length = len(message)
            
            # Calculate required LSB count
            lsb_count = LSBSteganographyService.calculate_required_lsb_count(message_length, img.size)
            if lsb_count is None:
                raise ValueError("Message too large for image (exceeds 4-LSB capacity)")

            # Convert message to binary
            binary_msg = ''.join(format(ord(c), '08b') for c in message)
            total_bits = len(binary_msg)

            # Create LSB mask and clear mask based on LSB count
            lsb_mask = (1 << lsb_count) - 1  # Creates a mask of required 1s
            clear_mask = ~lsb_mask & 0xFF    # Creates a mask to clear the LSBs

            # Embed message
            flat_img = img.reshape(-1)
            data_idx = 0
            bits_per_pixel = lsb_count
            
            for i in range(0, len(flat_img), 1):
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

            # Embed LSB count in the last pixel's channels
            img.reshape(-1)[-3:] = [lsb_count, 0, 0]  # Store LSB count in last pixel

            # Save encoded image
            encoded_path = os.path.join(temp_dir, "encoded_" + os.path.basename(upload_path))
            cv2.imwrite(encoded_path, img)
            
            # Cleanup
            os.unlink(upload_path)
            
            return encoded_path
            
        except Exception as e:
            if os.path.exists(upload_path):
                os.unlink(upload_path)
            raise e

    @staticmethod
    def decode(image_file, temp_dir):
        """Decodes a message from an image using stored LSB count"""
        try:
            # Save uploaded file
            upload_path = os.path.join(temp_dir, "uploaded_" + image_file.filename)
            image_file.save(upload_path)

            # Read image
            img = cv2.imread(upload_path)
            if img is None:
                raise ValueError("Invalid image file")

            # Get LSB count from last pixel
            lsb_count = img.reshape(-1)[-3]  # Get LSB count from last pixel
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
                        break

            # Cleanup
            os.unlink(upload_path)
            
            return decoded_text
            
        except Exception as e:
            if os.path.exists(upload_path):
                os.unlink(upload_path)
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
        encoded_path = LSBSteganographyService.encode(
            image_file=request.files['image'],
            message=request.form.get('message', ''),
            temp_dir=app.config['TEMP_DIR']
        )
        return jsonify({"encoded_image": encoded_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/decode', methods=['POST'])
def handle_decode():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
        
    try:
        message = LSBSteganographyService.decode(
            image_file=request.files['image'],
            temp_dir=app.config['TEMP_DIR']
        )
        return jsonify({"decoded_message": message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)