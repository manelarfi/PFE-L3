import os
import cv2
import numpy as np
import pywt

class DWTSteganographyService:
    @staticmethod
    def text_to_bits(text: str) -> str:
        text += '\0'  # null terminator
        return ''.join(f'{ord(c):08b}' for c in text)

    @staticmethod
    def bits_to_text(bits: str) -> str:
        message = ''
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) < 8:
                break
            c = chr(int(byte, 2))
            if c == '\0':
                break
            message += c
        return message

    @staticmethod
    def build_safe_mask(LL_f, LH_f, HL_f, HH_f, Y_orig, Δ=1):
        H2, W2 = LL_f.shape

        masks = {
            'LL': np.zeros_like(LL_f, bool),
            'LH': np.zeros_like(LH_f, bool),
            'HL': np.zeros_like(HL_f, bool),
            'HH': np.zeros_like(HH_f, bool),
        }

        for name, subband in masks.items():

            mask = masks[name]
            signs = {
                'LL': ( 1,  1,  1,  1),
                'LH': ( 1, -1,  1, -1),
                'HL': ( 1,  1, -1, -1),
                'HH': ( 1, -1, -1,  1),
            }[name]
            for p in range(H2):
                for q in range(W2):
                    y00 = Y_orig[2*p  , 2*q  ]
                    y10 = Y_orig[2*p+1, 2*q  ]
                    y01 = Y_orig[2*p  , 2*q+1]
                    y11 = Y_orig[2*p+1, 2*q+1]

                    delta = Δ/2.0
                    y00n = y00 + signs[0]*delta
                    y10n = y10 + signs[1]*delta
                    y01n = y01 + signs[2]*delta
                    y11n = y11 + signs[3]*delta
                    if all(0 <= y < 256 for y in (y00n, y10n, y01n, y11n)):
                        mask[p, q] = True

        return masks['LL'], masks['LH'], masks['HL'], masks['HH']

    @staticmethod
    def transform_DWT_float(Y: np.ndarray):
        return pywt.dwt2(Y, 'haar')  # returns LL_f, (LH_f, HL_f, HH_f)

    @staticmethod
    def transform_DWT_int(LL_f, LH_f, HL_f, HH_f):
        return (
            np.round(LL_f).astype(np.int32),
            np.round(LH_f).astype(np.int32),
            np.round(HL_f).astype(np.int32),
            np.round(HH_f).astype(np.int32),
        )

    @staticmethod
    def transform_IDWT(LL_i, LH_i, HL_i, HH_i, Cb, Cr):
        Y = pywt.idwt2((LL_i, (LH_i, HL_i, HH_i)), 'haar')
        Y = np.clip(Y, 0, 255).astype(np.uint8)

        print(f"Shape of Y: {Y.shape}, dtype: {Y.dtype}")
        # It's good practice to check if Cb or Cr are None before accessing .shape or .dtype
        if Cb is not None:
            print(f"Shape of Cb: {Cb.shape}, dtype: {Cb.dtype}")
        else:
            print("Cb is None!")
            # Handle this case, maybe raise an error or return
        if Cr is not None:
            print(f"Shape of Cr: {Cr.shape}, dtype: {Cr.dtype}")
        else:
            print("Cr is None!")
            # Handle this case

        # --- FIXES START HERE ---

        # 1. Ensure Cb and Cr have the same dimensions as Y
        target_height, target_width = Y.shape[:2]

        if Cb is not None and Cb.shape[:2] != (target_height, target_width):
            print(f"Resizing Cb from {Cb.shape[:2]} to ({target_height}, {target_width})")
            Cb = cv2.resize(Cb, (target_width, target_height), interpolation=cv2.INTER_LINEAR) # Or INTER_CUBIC

        if Cr is not None and Cr.shape[:2] != (target_height, target_width):
            print(f"Resizing Cr from {Cr.shape[:2]} to ({target_height}, {target_width})")
            Cr = cv2.resize(Cr, (target_width, target_height), interpolation=cv2.INTER_LINEAR) # Or INTER_CUBIC

        # 2. Ensure Cb and Cr have the same data type as Y (np.uint8)
        if Cb is not None and Cb.dtype != Y.dtype:
            print(f"Converting Cb dtype from {Cb.dtype} to {Y.dtype}")
            Cb = Cb.astype(Y.dtype)

        if Cr is not None and Cr.dtype != Y.dtype:
            print(f"Converting Cr dtype from {Cr.dtype} to {Y.dtype}")
            Cr = Cr.astype(Y.dtype)

        # --- FIXES END HERE ---

        # Defensive check after corrections
        if Cb is None or Cr is None:
            raise ValueError("Cb or Cr channel is None after processing attempts.")
        if not (Y.shape == Cb.shape == Cr.shape):
             raise ValueError(f"Dimension mismatch after attempting correction: Y:{Y.shape}, Cb:{Cb.shape}, Cr:{Cr.shape}")
        if not (Y.dtype == Cb.dtype == Cr.dtype):
             raise ValueError(f"Dtype mismatch after attempting correction: Y:{Y.dtype}, Cb:{Cb.dtype}, Cr:{Cr.dtype}")


        ycrcb = cv2.merge((Y, Cb, Cr))
        return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

    @staticmethod
    def encode(image_file, message: str, temp_dir: str) -> bytes:
        data = np.frombuffer(image_file.read(), np.uint8)
        image = cv2.imdecode(data, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Invalid image upload")

        # split YCrCb and cast each to float32
        ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        Yf, Cbf, Crf = cv2.split(ycrcb)
        Yf = Yf.astype(np.float32)
        Cbf = Cbf.astype(np.uint8)
        Crf = Crf.astype(np.uint8)

        # float DWT
        LL_f, (LH_f, HL_f, HH_f) = DWTSteganographyService.transform_DWT_float(Yf)

        # original Y for safety mask
        Y_orig = pywt.idwt2((LL_f, (LH_f, HL_f, HH_f)), 'haar')

        # build masks
        safe_LL, safe_LH, safe_HL, safe_HH = DWTSteganographyService.build_safe_mask(
            LL_f, LH_f, HL_f, HH_f, Y_orig, Δ=1)

        # int DWT for embedding
        LL_i, LH_i, HL_i, HH_i = DWTSteganographyService.transform_DWT_int(
            LL_f, LH_f, HL_f, HH_f)

        # prepare bitstream
        bits = DWTSteganographyService.text_to_bits(message)
        bit_idx = 0

        def embed_band(band, mask):
            nonlocal bit_idx
            flat = band.flatten()
            for i in np.argwhere(mask.flatten()):
                if bit_idx >= len(bits):
                    break
                b = int(bits[bit_idx])
                flat[i[0]] = (flat[i[0]] & ~1) | b
                bit_idx += 1
            return flat.reshape(band.shape)

        # embed
        HH_i = embed_band(HH_i, safe_HH)
        if bit_idx < len(bits):
            HL_i = embed_band(HL_i, safe_HL)
        if bit_idx < len(bits):
            LH_i = embed_band(LH_i, safe_LH)
        if bit_idx < len(bits):
            raise ValueError("Message too long to embed losslessly")

        # reconstruct
        stego = DWTSteganographyService.transform_IDWT(LL_i, LH_i, HL_i, HH_i, Cbf, Crf)
        
        # Convert to bytes
        success, buffer = cv2.imencode('.png', stego)
        if not success:
            raise IOError("Failed to encode image")
        return buffer.tobytes()

    @staticmethod
    def decode(image_file) -> str:
        data = np.frombuffer(image_file.read(), np.uint8)
        image = cv2.imdecode(data, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Invalid image upload")

        ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        Yf, Cbf, Crf = cv2.split(ycrcb)
        Yf = Yf.astype(np.float32)

        LL_f, (LH_f, HL_f, HH_f) = DWTSteganographyService.transform_DWT_float(Yf)
        Y_orig = pywt.idwt2((LL_f, (LH_f, HL_f, HH_f)), 'haar')
        safe_LL, safe_LH, safe_HL, safe_HH = DWTSteganographyService.build_safe_mask(
            LL_f, LH_f, HL_f, HH_f, Y_orig, Δ=1)

        LL_i, LH_i, HL_i, HH_i = DWTSteganographyService.transform_DWT_int(
            LL_f, LH_f, HL_f, HH_f)

        bits = []
        def extract_band(band, mask):
            for i in np.argwhere(mask.flatten()):
                bits.append(str(int(band.flatten()[i[0]]) & 1))

        extract_band(HH_i, safe_HH)
        extract_band(HL_i, safe_HL)
        extract_band(LH_i, safe_LH)

        return DWTSteganographyService.bits_to_text(''.join(bits))
