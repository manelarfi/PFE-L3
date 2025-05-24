import os
import cv2
import numpy as np
import pywt
from typing import List, Tuple, Union

# Define where temporary key matrices are stored
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_DIR = os.path.normpath(os.path.join(MODULE_DIR, '..', 'tmp'))

class DWTSteganographyService:
    """
    Implements Varying Mode Case 1 steganography using 1-level Haar DWT.
    Provides encode and decode methods that handle key matrix computation.
    """
    PAIR_COUNTS = {0: 1, 1: 6, 2: 4, 3: 2}
    EXTRA_BITS = {6: (2, 1), 4: (2, 0), 2: (1, 0), 1: (0, 0)}
    KEY_MAPPING = {0: 0.00, 1: 0.25, 2: -0.50, 3: -0.25}

    @classmethod
    def encode(cls, cover_img: np.ndarray, bitstream: Union[List[int], np.ndarray]) -> Tuple[np.ndarray, np.ndarray]:
        # Normalize bitstream to list
        if isinstance(bitstream, np.ndarray):
            bitstream = bitstream.astype(int).tolist()
        else:
            bitstream = list(bitstream)

        # 1-level DWT
        LL, (LH, HL, HH) = pywt.dwt2(cover_img.astype(float), 'haar')
        LH = np.round(LH).astype(np.int32)
        HL = np.round(HL).astype(np.int32)
        HH = np.round(HH).astype(np.int32)

        M, N = HH.shape
        max_coeffs = M * N

        # Prepare differential values
        symbols = [int(f"{bitstream[i]}{bitstream[i+1]}", 2)
                   for i in range(0, min(len(bitstream), 2*max_coeffs), 2)]
        diffs = [(symbols[i+1] - symbols[i]) for i in range(0, len(symbols)-1, 2)]
        diffs = diffs[:max_coeffs]

        extra_start = 2 * max_coeffs
        idx = 0
        for i in range(M):
            for j in range(N):
                if idx >= len(diffs):
                    break
                a = abs(diffs[idx])
                HH[i, j] = (HH[i, j] & ~0b11) | a

                n_lh, n_hl = cls.EXTRA_BITS[cls.PAIR_COUNTS[a]]
                needed = n_lh + n_hl
                start = extra_start + idx * needed
                extras = bitstream[start:start+needed]
                if len(extras) < needed:
                    extras += [0] * (needed - len(extras))

                for k in range(n_lh):
                    LH[i, j] = (LH[i, j] & ~1) | extras[k]
                for k in range(n_hl):
                    HL[i, j] = (HL[i, j] & ~1) | extras[n_lh + k]

                idx += 1
            if idx >= len(diffs):
                break

        stego_float = pywt.idwt2((LL.astype(float), (LH.astype(float), HL.astype(float), HH.astype(float))), 'haar')
        key_matrix = stego_float - np.floor(stego_float)
        stego_uint8 = np.clip(np.round(stego_float), 0, 255).astype(np.uint8)
        return stego_uint8, key_matrix

    @classmethod
    def decode(cls, stego_img_path: str, key_filename: str) -> List[int]:
        """
        Extract bits from stego image file and a key matrix stored in tmp folder.
        :param stego_img_path: Path to the stego PNG file (grayscale)
        :param key_filename: Filename of the .npy key matrix in tmp/
        :returns: Recovered bitstream
        """
        # Load stego image
        stego = cv2.imread(stego_img_path, cv2.IMREAD_GRAYSCALE)
        if stego is None:
            raise FileNotFoundError(f"Stego image not found: {stego_img_path}")

        # Load key matrix from tmp dir
        key_path = os.path.join(TMP_DIR, key_filename)
        if not os.path.isfile(key_path):
            raise FileNotFoundError(f"Key matrix not found: {key_path}")
        key_matrix = np.load(key_path)

        # Reconstruct float-domain image
        F = stego.astype(float)
        K_prime = np.vectorize(cls.KEY_MAPPING.get)(key_matrix.astype(int))
        E = F + K_prime

        # DWT
        LL, (LH, HL, HH) = pywt.dwt2(E, 'haar')
        LH = np.round(LH).astype(np.int32)
        HL = np.round(HL).astype(np.int32)
        HH = np.round(HH).astype(np.int32)

        bits_main, bits_extra = [], []
        M, N = HH.shape
        for i in range(M):
            for j in range(N):
                a = int(HH[i, j]) & 0b11
                bits_main.extend([(a >> 1) & 1, a & 1])
                n_lh, n_hl = cls.EXTRA_BITS[cls.PAIR_COUNTS[a]]
                for _ in range(n_lh): bits_extra.append(int(LH[i, j]) & 1)
                for _ in range(n_hl): bits_extra.append(int(HL[i, j]) & 1)

        return bits_main + bits_extra

# Example usage:
# stego, key = DWTSteganographyService.encode(cover_img, bitstream)
# recovered = DWTSteganographyService.decode('tmp/stego_xxx.png', 'key_xxx.npy')
