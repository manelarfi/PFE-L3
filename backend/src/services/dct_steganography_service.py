import cv2
import numpy as np
from PIL import Image


Q50 = np.array([
    [16,11,10,16,24,40,51,61],
    [12,12,14,19,26,58,60,55],
    [14,13,16,24,40,57,69,56],
    [14,17,22,29,51,87,80,62],
    [18,22,37,56,68,109,103,77],
    [24,35,55,64,81,104,113,92],
    [49,64,78,87,103,121,120,101],
    [72,92,95,98,112,100,103,99]
])


class DCTSteganographyService:

    '''@staticmethod
    def _message_to_bits(message):
        """Convertit un message en une chaîne de bits"""
        return ''.join(format(ord(c), '08b') for c in message)

    @staticmethod
    def _bits_to_message(bits):
        """Convertit une chaîne de bits en message"""
        chars = []
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) < 8:
                break
            chars.append(chr(int(byte, 2)))
            if ''.join(chars).endswith("#####"):
                break
        return ''.join(chars).replace("#####", "")'''




    @staticmethod
    def encode_dct_jpeg_like(image_file, message) -> bytes:
        # Read image from file object
        data = np.frombuffer(image_file.read(), np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Invalid image upload")

        ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        Y, Cr, Cb = cv2.split(ycrcb)
        Y = np.float32(Y)
        #print("[DEBUG] Y channel converted to float32.")
        message += "#####"
        bits = ''.join(format(ord(c), '08b') for c in message)
        #print(f"[DEBUG] Message to encode: {message}")
        #print(f"[DEBUG] Bits to encode ({len(bits)} bits): {bits}")

        idx = 0

        for i in range(0, Y.shape[0] - 8 + 1, 8):
            for j in range(0, Y.shape[1] - 8 + 1, 8):
                if idx >= len(bits):
                    break

                block = Y[i:i+8, j:j+8]
                dct = cv2.dct(block)
                quantized = np.round(dct / Q50)
                bit_to_embed = int(bits[idx])
                old_coeff = quantized[3, 3]
                coeff = int(old_coeff)
                coeff = (coeff & ~1) | int(bits[idx])
                quantized[3, 3] = coeff
                idx += 1

                dequantized = quantized * Q50
                idct_block = cv2.idct(dequantized)
                Y[i:i+8, j:j+8] = np.clip(idct_block, 0, 255)

            if idx >= len(bits):
                break

        Y = np.uint8(Y)
        stego_ycrcb = cv2.merge((Y, Cr, Cb))
        stego_bgr = cv2.cvtColor(stego_ycrcb, cv2.COLOR_YCrCb2BGR)
        
        # Convert to bytes
        success, buffer = cv2.imencode('.png', stego_bgr)
        if not success:
            raise IOError("Failed to encode image")
        #print(f"[INFO] Encoding complete. {idx} bits encoded.")
        return buffer.tobytes()



    @staticmethod
    def decode_dct_jpeg_like(image_file):
        # Read image from file object
        data = np.frombuffer(image_file.read(), np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Invalid image upload")

        ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        Y = np.float32(ycrcb[:, :, 0])

        bits = ""
        for i in range(0, Y.shape[0] - 8 + 1, 8):
            for j in range(0, Y.shape[1] - 8 + 1, 8):
                block = Y[i:i+8, j:j+8]
                dct = cv2.dct(block)
                quantized = np.round(dct / Q50)
                coeff = int(quantized[3, 3])
                bits += str(coeff & 1)
                 
                if len(bits) % 8 == 0:
                    chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
                    joined = ''.join(chars)
                    if "#####" in joined:
                        return joined.replace("#####", "")
        
        return "[ERREUR] Message non trouvé"


# if __name__ == "__main__":
#     # Exemple d'encodage
#     DCTSteganographyService.encode_dct_jpeg_like(
#         image_path='image.jpg',
#         message='Hi jazzyyyyyyyyy!',
#         output_path='image_stego.jpg'
#     )

#     # Exemple de décodage
#     message = DCTSteganographyService.decode_dct_jpeg_like('image_stego.jpg')
#     print("[INFO] Message décodé :", message)
