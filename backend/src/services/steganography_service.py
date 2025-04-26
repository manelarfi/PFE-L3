import cv2
import numpy as np
import tempfile
import os

class SteganographyService:
    
    @staticmethod
    def encode(image_file, message):
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
            image_path = tmp.name
            image_file.save(image_path)

        # Read the image using OpenCV
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Invalid image file")

        # Prepare the message
        message += '#####'  # delimiter to indicate the end of the hidden message
        binary_message = ''.join(format(ord(c), '08b') for c in message)

        data_index = 0
        total_bits = len(binary_message)

        # Get image dimensions
        rows, cols, channels = img.shape

        # Iterate through each pixel
        for row in range(rows):
            for col in range(cols):
                pixel = img[row, col]
                for channel in range(3):  # B, G, R
                    if data_index < total_bits:
                        pixel[channel] = (pixel[channel] & ~1) | int(binary_message[data_index])
                        data_index += 1
                    if data_index >= total_bits:
                        break
                if data_index >= total_bits:
                    break
            if data_index >= total_bits:
                break

        # Save the encoded image
        encoded_image_path = os.path.join(tempfile.gettempdir(), "encoded_image.png")
        cv2.imwrite(encoded_image_path, img)

        return encoded_image_path

    @staticmethod
    def decode(image_file):
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
            image_path = tmp.name
            image_file.save(image_path)

        # Read the image using OpenCV
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Invalid image file")

        binary_message = ''
        rows, cols, channels = img.shape

        # Extract LSBs
        for row in range(rows):
            for col in range(cols):
                pixel = img[row, col]
                for channel in range(3):  # B, G, R
                    binary_message += str(pixel[channel] & 1)

        # Group binary string into characters
        decoded_message = ''
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i+8]
            character = chr(int(byte, 2))
            decoded_message += character
            if decoded_message.endswith('#####'):
                break

        # Remove delimiter
        return decoded_message.replace('#####', '')
