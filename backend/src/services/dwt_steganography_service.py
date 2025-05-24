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
        print(Y_orig)
        print('\n')
        masks = {
            'LL': np.zeros_like(LL_f, bool),
            'LH': np.zeros_like(LH_f, bool),
            'HL': np.zeros_like(HL_f, bool),
            'HH': np.zeros_like(HH_f, bool),
        }
        print(masks)
        print('\n')

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
        ycrcb = cv2.merge((Y, Cb, Cr))
        return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

    @staticmethod
    def encode(image_file, message: str, temp_dir: str) -> str:
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
        print("bits", bits)

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
        # if bit_idx < len(bits):
        #     LL_i = embed_band(LL_i, safe_LL)
        if bit_idx < len(bits):
            raise ValueError("Message too long to embed losslessly")

        # reconstruct & save
        stego = DWTSteganographyService.transform_IDWT(LL_i, LH_i, HL_i, HH_i, Cbf, Crf)
        os.makedirs(temp_dir, exist_ok=True)
        out_path = os.path.join(temp_dir, "stego_image.png")
        if not cv2.imwrite(out_path, stego):
            raise IOError("Failed to write stego image")
        return out_path

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
        # extract_band(LL_i, safe_LL)

        return DWTSteganographyService.bits_to_text(''.join(bits))
