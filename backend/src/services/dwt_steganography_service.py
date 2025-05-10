import cv2
import numpy as np
import pywt
import os

class DWTSteganographyService:

    @staticmethod
    def encode(image_file, message, temp_dir):
        """DWT-based encoding implementation"""
        try:
            # Save uploaded file
            upload_path = os.path.join(temp_dir, "dwt_upload_" + image_file.filename)
            image_file.save(upload_path)

            # Read and validate image
            img = cv2.imread(upload_path)
            if img is None:
                raise ValueError("Invalid image file")

            # Convert to YCrCb and process Y channel
            ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
            Y = ycrcb[:,:,0].astype(np.float32)

            # 2-level DWT decomposition
            coeffs = pywt.wavedec2(Y, 'haar', level=2)
            cA2, (cH2, cV2, cD2), (cH1, cV1, cD1) = coeffs

            # Prepare message with delimiter and calculate binary message
            message += '#####'  # Delimiter to mark the end of the message
            binary_msg = ''.join(format(ord(c), '08b') for c in message)
            total_bits = len(binary_msg)

            # Embed in cH1 coefficients
            flat_cH1 = cH1.flatten()
            if total_bits > len(flat_cH1):
                raise ValueError(f"Message too large. Max capacity: {len(flat_cH1)} bits")

            # Modify the coefficients
            for i in range(total_bits):
                int_val = int(flat_cH1[i])
                flat_cH1[i] = (int_val & ~1) | int(binary_msg[i])

            # Reshape modified coefficients back to their original shape
            modified_cH1 = flat_cH1[:len(cH1.flatten())].reshape(cH1.shape)
            
            # Reconstruct image with modified coefficients
            new_coeffs = (cA2, (cH2, cV2, cD2), (modified_cH1, cV1, cD1))
            Y_modified = pywt.waverec2(new_coeffs, 'haar')

            # Ensure Y values are within the valid image range
            ycrcb[:,:,0] = np.clip(Y_modified, 0, 255).astype(np.uint8)

            # Convert back to BGR
            stego_img = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

            # Save result
            encoded_path = os.path.join(temp_dir, "dwt_encoded_" + image_file.filename)
            cv2.imwrite(encoded_path, stego_img)

            os.unlink(upload_path)
            return encoded_path

        except Exception as e:
            if os.path.exists(upload_path):
                os.unlink(upload_path)
            raise e

    @staticmethod
    def decode(image_file, temp_dir):
        """DWT-based decoding implementation"""
        try:
            # Save uploaded file
            upload_path = os.path.join(temp_dir, "dwt_upload_" + image_file.filename)
            image_file.save(upload_path)

            # Read image
            img = cv2.imread(upload_path)
            if img is None:
                raise ValueError("Invalid image file")

            # Process Y channel
            ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
            Y = ycrcb[:,:,0].astype(np.float32)

            # DWT decomposition
            coeffs = pywt.wavedec2(Y, 'haar', level=2)
            cA2, (cH2, cV2, cD2), (cH1, cV1, cD1) = coeffs

            # Extract LSBs from cH1
            binary_msg = ''.join(str(int(coeff) & 1) for coeff in cH1.flatten())

            # Convert binary message back to string
            decoded_msg = ''
            for i in range(0, len(binary_msg), 8):
                byte = binary_msg[i:i+8]
                if len(byte) < 8:
                    break
                decoded_msg += chr(int(byte, 2))
                if decoded_msg.endswith('#####'):
                    break

            os.unlink(upload_path)
            return decoded_msg.replace('#####', '')

        except Exception as e:
            if os.path.exists(upload_path):
                os.unlink(upload_path)
            raise e
