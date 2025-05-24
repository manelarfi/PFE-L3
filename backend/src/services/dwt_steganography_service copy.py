import os
import cv2
import numpy as np
import pywt

class DWTSteganographyService:
    @staticmethod
    def text_to_bits(text):
        # Add a null character to mark the end of the message
        text += '\0'
        return ''.join(f'{ord(c):08b}' for c in text)
    
    @staticmethod
    def bits_to_text(bits):
        chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
        message = ''
        for byte in chars:
            if len(byte) < 8:
                break
            char = chr(int(byte, 2))
            if char == '\0':  # stop at null terminator
                break
            message += char
        return message
    
    @staticmethod
    def embed_bits_safe(coefficients, bits, k=1, start_idx=0, safe_margin=150):
        flat = coefficients.flatten()
        bit_idx = start_idx
        print(bit_idx)
        for i in range(len(flat)):
            if abs(flat[i]) > safe_margin:
                continue
            # if bit_idx + k > len(bits):
            #     break
            bit_chunk = bits[bit_idx:bit_idx + k].ljust(k, '0')
            print("EMBEDDIIIIING")
            bit_value = int(bit_chunk, 2)
            flat[i] = (int(flat[i]) & ~((1 << k) - 1)) | bit_value
            bit_idx += k
            print("the embedding in :", flat[i])
        return flat.reshape(coefficients.shape), bit_idx

    @staticmethod
    def extract_bits_safe(coefficients, total_bits, k=1, start_idx=0, safe_margin=250):
        flat = coefficients.flatten()
        print("flat", flat)
        bit_idx = start_idx
        extracted_bits = ''

        for i in range(len(flat)):
            if abs(flat[i]) > safe_margin:
                continue
            # if bit_idx + k > total_bits:
            #     break
            value = flat[i]
            print("EXTRACTING :", value)
            extracted = value & ((1 << k) - 1)
            extracted_bits += f'{extracted:0{k}b}'
            bit_idx += k
        return extracted_bits

    @staticmethod
    def transform_DWT(image):
        ycrcb_image = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        Y, Cb, Cr = cv2.split(ycrcb_image)
        print("Y before embedding", Y)
        coeffs = pywt.dwt2(Y, 'haar')
        LL, (LH, HL, HH) = coeffs

        LL_i = np.round(LL).astype(np.int32)
        LH_i = np.round(LH).astype(np.int32)
        HL_i = np.round(HL).astype(np.int32)
        HH_i = np.round(HH).astype(np.int32)
        return LL_i, LH_i, HL_i, HH_i, Cb, Cr

    @staticmethod
    def transform_IDWT(LL, LH, HL, HH, Cb, Cr):
        coeffs = LL, (LH, HL, HH)
        Y = pywt.idwt2(coeffs, 'haar')
        print("Y after embedding", Y)
        Y = DWTSteganographyService.safe_round_preserve_lsb(Y, k=3)
        print("Y after rounding", Y)
        Y = np.clip(Y, 0, 255).astype(np.uint8)
        print("Y after clipping", Y)
        ycrcb_image = cv2.merge((Y, Cb, Cr))
        print(ycrcb_image)
        image = cv2.cvtColor(ycrcb_image, cv2.COLOR_YCrCb2BGR)
        print("IMAGE RECONSTRU", image)

        print("-------------------PETIT TEST-------------------")
        LL, LH, HL, HH, Cb, Cr = DWTSteganographyService.transform_DWT(image) 
        return image
    
    @staticmethod
    def safe_round_preserve_lsb(float_array, k=3):
        int_array = np.round(float_array).astype(np.int32)
        flat_float = float_array.flatten()
        flat_int = int_array.flatten()

        for i in range(len(flat_float)):
            original = int(flat_float[i])  # truncate to int
            rounded = flat_int[i]

            # Extract the last k bits from the original (before rounding)
            lsb_mask = (1 << k) - 1
            preserved_bits = original & lsb_mask

            # Clear last k bits of the rounded value and restore the preserved bits
            flat_int[i] = (rounded & ~lsb_mask) | preserved_bits

        return flat_int.reshape(float_array.shape)

    @staticmethod
    def encode(image_file, message, temp_dir):
        # Read image from file-like object
        file_bytes = np.frombuffer(image_file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if image is None:
            raise ValueError("Failed to decode image. Please ensure a valid image file was uploaded.")

        message_bits = DWTSteganographyService.text_to_bits(message)
        print("message bits", message_bits)
        LL, LH, HL, HH, Cb, Cr = DWTSteganographyService.transform_DWT(image)

        bit_idx = 0
        print("before embedding LL", LL)
        LL, bit_idx = DWTSteganographyService.embed_bits_safe(LL, message_bits, k=3, start_idx=bit_idx)
        print("after ma embeddina LL", LL)
        if bit_idx < len(message_bits):
            print("before embedding LH", LH)
            LH, bit_idx = DWTSteganographyService.embed_bits_safe(LH, message_bits, k=3, start_idx=bit_idx)
            print("after ma embeddina LH", LH)
        if bit_idx < len(message_bits):
            print("before embedding HL", HL)
            HL, bit_idx = DWTSteganographyService.embed_bits_safe(HL, message_bits, k=3, start_idx=bit_idx)
            print("after ma embeddina HL", HL)
        if bit_idx < len(message_bits):
            print("before embedding HH", HH)
            HH, bit_idx = DWTSteganographyService.embed_bits_safe(HH, message_bits, k=3, start_idx=bit_idx)
            print("after ma embeddina HH", HH)

        if bit_idx < len(message_bits):
            raise ValueError("Message is too long to be embedded in the image.")

        stego_image = DWTSteganographyService.transform_IDWT(LL, LH, HL, HH, Cb, Cr)
        output_path = os.path.join(temp_dir, "stego_image.png")

        cv2.imwrite(output_path, stego_image)
        return output_path
    

    @staticmethod
    def decode(image_file):
        # Read image from file-like object
        file_bytes = np.frombuffer(image_file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if image is None:
            raise ValueError("Failed to decode image. Please ensure a valid image file was uploaded.")

        LL, LH, HL, HH, Cb, Cr = DWTSteganographyService.transform_DWT(image)

        # We estimate total bits by number of coefficients * k (3 bits per coeff)
        total_coeffs = LL.size + LH.size + HL.size + HH.size
        total_bits = total_coeffs * 3

        bits = ''
        print("extractiong men LL", LL)
        bits += DWTSteganographyService.extract_bits_safe(LL, total_bits, k=3)
        print("extractiong men LH", LH)
        bits += DWTSteganographyService.extract_bits_safe(LH, total_bits, k=3, start_idx=len(bits))
        print("extractiong men HL", HL)
        bits += DWTSteganographyService.extract_bits_safe(HL, total_bits, k=3, start_idx=len(bits))
        print("extractiong men HH", HH)
        bits += DWTSteganographyService.extract_bits_safe(HH, total_bits, k=3, start_idx=len(bits))

        print("extracted bits", bits)
        return DWTSteganographyService.bits_to_text(bits)
