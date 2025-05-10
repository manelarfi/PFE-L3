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
    def encode(image_file, message, temp_dir):
        """Encodes a message into an image and saves to temp_dir"""
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
            binary_msg = ''.join(format(ord(c), '08b') for c in message)
            total_bits = len(binary_msg)

            # Validate capacity
            if total_bits > img.size * 3:
                raise ValueError("Message too large for image")

            # Embed message
            flat_img = img.reshape(-1, 3)
            data_idx = 0
            
            for pixel in flat_img:
                for channel in range(3):
                    if data_idx < total_bits:
                        pixel[channel] = np.uint8((pixel[channel] & 0xFE) | int(binary_msg[data_idx]))
                        data_idx += 1
                    else:
                        break
                if data_idx >= total_bits:
                    break

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
        """Decodes a message from an image in temp_dir"""
        try:
            # Save uploaded file
            upload_path = os.path.join(temp_dir, "uploaded_" + image_file.filename)
            image_file.save(upload_path)

            # Read image
            img = cv2.imread(upload_path)
            if img is None:
                raise ValueError("Invalid image file")

            # Extract LSBs
            binary_msg = ''.join(str(pixel & 1) for pixel in img.reshape(-1))

            # Convert to string
            decoded_msg = ''
            for i in range(0, len(binary_msg), 8):
                byte = binary_msg[i:i+8]
                if len(byte) < 8:
                    break
                decoded_msg += chr(int(byte, 2))
                if decoded_msg.endswith('#####'):
                    break

            # Cleanup
            os.unlink(upload_path)
            
            return decoded_msg.replace('#####', '')
            
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