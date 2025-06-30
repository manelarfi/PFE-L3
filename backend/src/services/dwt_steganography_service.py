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
    def save_analysis_data(masks, operation, positions=None):
        """Save masks and embedding/extraction positions to files for analysis"""
        # Create analysis directory if it doesn't exist
        analysis_dir = os.path.join(os.getcwd(), 'analysis')
        if not os.path.exists(analysis_dir):
            os.makedirs(analysis_dir)

        # Save masks
        for name, mask in masks.items():
            # Save safe mask matrix
            mask_filename = os.path.join(analysis_dir, f'mask_{operation}_{name}.txt')
            np.savetxt(mask_filename, mask.astype(int), fmt='%d')
            
            # Calculate and print statistics
            total = mask.size
            safe = np.sum(mask)
            print(f"{operation} - {name} mask statistics:")
            print(f"Total positions: {total}")
            print(f"Safe positions: {safe}")
            print(f"Safety ratio: {(safe/total)*100:.2f}%")
            print(f"Saved to: {mask_filename}")
            
            # Save embedding/extraction positions if available
            if positions is not None and name in positions:
                pos_filename = os.path.join(analysis_dir, f'{operation}_positions_{name}.txt')
                np.savetxt(pos_filename, positions[name].astype(int), fmt='%d')
                used = np.sum(positions[name])
                print(f"{operation} positions for {name}:")
                print(f"Used positions: {used}")
                print(f"Usage ratio: {(used/total)*100:.2f}%")
                print(f"Saved to: {pos_filename}")

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

        # Save the safe masks for analysis
        DWTSteganographyService.save_analysis_data(masks, 'safe_mask')
        return masks['LL'], masks['LH'], masks['HL'], masks['HH']

    @staticmethod
    def transform_DWT_float(Y: np.ndarray):
        # Normalize input values to reduce filter impact
        Y_norm = Y / 255.0
        
        # First level DWT
        coeffs1 = pywt.dwt2(Y_norm, 'haar')
        LL1 = coeffs1[0]
        LH1, HL1, HH1 = coeffs1[1]
        
        # Second level DWT
        coeffs2 = pywt.dwt2(LL1, 'haar')
        LL2 = coeffs2[0]
        LH2, HL2, HH2 = coeffs2[1]
        
        # Third level DWT
        coeffs3 = pywt.dwt2(LL2, 'haar')
        LL3 = coeffs3[0]
        LH3, HL3, HH3 = coeffs3[1]
        
        # Denormalize all coefficients
        return {
            'level1': {
                'LL': LL1 * 255.0,
                'LH': LH1 * 255.0,
                'HL': HL1 * 255.0,
                'HH': HH1 * 255.0
            },
            'level2': {
                'LL': LL2 * 255.0,
                'LH': LH2 * 255.0,
                'HL': HL2 * 255.0,
                'HH': HH2 * 255.0
            },
            'level3': {
                'LL': LL3 * 255.0,
                'LH': LH3 * 255.0,
                'HL': HL3 * 255.0,
                'HH': HH3 * 255.0
            }
        }

    @staticmethod
    def transform_DWT_int(subbands):
        # Quantization factor to reduce rounding errors
        Q = 1.0
        
        result = {}
        for level in ['level1', 'level2', 'level3']:
            result[level] = {
                'LL': np.round(subbands[level]['LL'] / Q).astype(np.int32) * Q,
                'LH': np.round(subbands[level]['LH'] / Q).astype(np.int32) * Q,
                'HL': np.round(subbands[level]['HL'] / Q).astype(np.int32) * Q,
                'HH': np.round(subbands[level]['HH'] / Q).astype(np.int32) * Q
            }
        return result

    @staticmethod
    def transform_IDWT(subbands, Cb, Cr):
        # Normalize coefficients before inverse transform
        # Start with level 3 (innermost)
        for level in ['level3', 'level2', 'level1']:
            LL_norm = subbands[level]['LL'] / 255.0
            LH_norm = subbands[level]['LH'] / 255.0
            HL_norm = subbands[level]['HL'] / 255.0
            HH_norm = subbands[level]['HH'] / 255.0
            
            # Perform inverse DWT for this level
            Y = pywt.idwt2((LL_norm, (LH_norm, HL_norm, HH_norm)), 'haar')
            
            # If not the last level, update the LL component of the next level
            if level != 'level1':
                next_level = f"level{int(level[-1])-1}"
                subbands[next_level]['LL'] = Y * 255.0
        
        # Final Y is the result of the last inverse transform
        Y = np.clip(Y * 255.0, 0, 255).astype(np.uint8)

        # Ensure dimensions match
        target_height, target_width = Y.shape[:2]

        if Cb is not None and Cb.shape[:2] != (target_height, target_width):
            Cb = cv2.resize(Cb, (target_width, target_height), interpolation=cv2.INTER_LINEAR)

        if Cr is not None and Cr.shape[:2] != (target_height, target_width):
            Cr = cv2.resize(Cr, (target_width, target_height), interpolation=cv2.INTER_LINEAR)

        # Ensure correct data type
        if Cb is not None:
            Cb = Cb.astype(np.uint8)
        if Cr is not None:
            Cr = Cr.astype(np.uint8)

        # Defensive checks
        if Cb is None or Cr is None:
            raise ValueError("Cb or Cr channel is None after processing attempts.")
        if not (Y.shape == Cb.shape == Cr.shape):
            raise ValueError(f"Dimension mismatch after attempting correction: Y:{Y.shape}, Cb:{Cb.shape}, Cr:{Cr.shape}")
        if not (Y.dtype == Cb.dtype == Cr.dtype):
            raise ValueError(f"Dtype mismatch after attempting correction: Y:{Y.dtype}, Cb:{Cb.dtype}, Cr:{Cr.dtype}")

        ycrcb = cv2.merge((Y, Cb, Cr))
        return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

    @staticmethod
    def save_subband_values(subbands, operation):
        """Save subband coefficient values to files for analysis"""
        # Create image directory if it doesn't exist
        image_dir = os.path.join(os.getcwd(), 'image')
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        # Save each subband's values
        for name, values in subbands.items():
            filename = os.path.join(image_dir, f'{operation}_subband_{name}.txt')
            np.savetxt(filename, values, fmt='%.6f')  # Use higher precision for float values
            print(f"Saved {operation} subband {name} values to: {filename}")

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
        subbands = DWTSteganographyService.transform_DWT_float(Yf)

        # Save original subband values
        DWTSteganographyService.save_subband_values(subbands['level1'], 'original')
        DWTSteganographyService.save_subband_values(subbands['level2'], 'original')
        DWTSteganographyService.save_subband_values(subbands['level3'], 'original')

        # original Y for safety mask
        Y_orig = pywt.idwt2((subbands['level1']['LL'], (subbands['level1']['LH'], subbands['level1']['HL'], subbands['level1']['HH'])), 'haar')

        # build masks
        safe_LL, safe_LH, safe_HL, safe_HH = DWTSteganographyService.build_safe_mask(
            subbands['level1']['LL'], subbands['level1']['LH'], subbands['level1']['HL'], subbands['level1']['HH'], Y_orig, Δ=1)

        # int DWT for embedding
        LL_i, LH_i, HL_i, HH_i = DWTSteganographyService.transform_DWT_int(
            subbands['level1']['LL'], subbands['level1']['LH'], subbands['level1']['HL'], subbands['level1']['HH'])

        # prepare bitstream
        bits = DWTSteganographyService.text_to_bits(message)
        bit_idx = 0

        # Create embedding position trackers
        embedding_positions = {
            'HH': np.zeros_like(safe_HH, dtype=bool),
            'HL': np.zeros_like(safe_HL, dtype=bool),
            'LH': np.zeros_like(safe_LH, dtype=bool),
            'LL': np.zeros_like(safe_LL, dtype=bool)
        }

        def embed_band(band, mask, band_name):
            nonlocal bit_idx
            flat = band.flatten()
            flat_positions = embedding_positions[band_name].flatten()
            for i in np.argwhere(mask.flatten()):
                if bit_idx >= len(bits):
                    break
                b = int(bits[bit_idx])
                flat[i[0]] = (flat[i[0]] & ~1) | b
                flat_positions[i[0]] = True  # Mark this position as used
                bit_idx += 1
            embedding_positions[band_name] = flat_positions.reshape(band.shape)
            return flat.reshape(band.shape)

        # embed
        HH_i = embed_band(HH_i, safe_HH, 'HH')
        if bit_idx < len(bits):
            HL_i = embed_band(HL_i, safe_HL, 'HL')
        if bit_idx < len(bits):
            LH_i = embed_band(LH_i, safe_LH, 'LH')
        if bit_idx < len(bits):
            raise ValueError("Message too long to embed losslessly")

        # Save modified subband values
        DWTSteganographyService.save_subband_values({
            'LL': LL_i,
            'LH': LH_i,
            'HL': HL_i,
            'HH': HH_i
        }, 'embedded')

        # Save embedding positions for analysis
        DWTSteganographyService.save_analysis_data(
            {'HH': safe_HH, 'HL': safe_HL, 'LH': safe_LH, 'LL': safe_LL},
            'embedding',
            embedding_positions
        )

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

        subbands = DWTSteganographyService.transform_DWT_float(Yf)

        # Save received subband values
        DWTSteganographyService.save_subband_values(subbands['level1'], 'received')
        DWTSteganographyService.save_subband_values(subbands['level2'], 'received')
        DWTSteganographyService.save_subband_values(subbands['level3'], 'received')

        Y_orig = pywt.idwt2((subbands['level1']['LL'], (subbands['level1']['LH'], subbands['level1']['HL'], subbands['level1']['HH'])), 'haar')

        safe_LL, safe_LH, safe_HL, safe_HH = DWTSteganographyService.build_safe_mask(
            subbands['level1']['LL'], subbands['level1']['LH'], subbands['level1']['HL'], subbands['level1']['HH'], Y_orig, Δ=1)

        LL_i, LH_i, HL_i, HH_i = DWTSteganographyService.transform_DWT_int(
            subbands['level1']['LL'], subbands['level1']['LH'], subbands['level1']['HL'], subbands['level1']['HH'])

        # Save extracted subband values
        DWTSteganographyService.save_subband_values({
            'LL': LL_i,
            'LH': LH_i,
            'HL': HL_i,
            'HH': HH_i
        }, 'extracted')

        # Create extraction position trackers
        extraction_positions = {
            'HH': np.zeros_like(safe_HH, dtype=bool),
            'HL': np.zeros_like(safe_HL, dtype=bool),
            'LH': np.zeros_like(safe_LH, dtype=bool),
            'LL': np.zeros_like(safe_LL, dtype=bool)
        }

        current_byte = []  # Store bits of current byte
        message_bits = []  # Store all extracted bits
        found_null = False

        def process_byte():
            nonlocal found_null
            if len(current_byte) == 8:
                byte_str = ''.join(current_byte)
                c = chr(int(byte_str, 2))
                if c == '\0':
                    found_null = True
                    return True
                message_bits.extend(current_byte)
                current_byte.clear()
            return False

        def extract_band(band, mask, band_name):
            nonlocal current_byte, found_null
            if found_null:
                return

            flat = band.flatten()
            flat_positions = extraction_positions[band_name].flatten()
            
            for i in np.argwhere(mask.flatten()):
                if found_null:
                    break
                    
                bit = str(int(flat[i[0]]) & 1)
                current_byte.append(bit)
                flat_positions[i[0]] = True
                
                # Process byte when we have 8 bits
                if process_byte():
                    break
                
            extraction_positions[band_name] = flat_positions.reshape(band.shape)

        # Extract and track positions
        extract_band(HH_i, safe_HH, 'HH')
        if not found_null:
            extract_band(HL_i, safe_HL, 'HL')
        if not found_null:
            extract_band(LH_i, safe_LH, 'LH')

        # Save extraction positions for analysis
        DWTSteganographyService.save_analysis_data(
            {'HH': safe_HH, 'HL': safe_HL, 'LH': safe_LH, 'LL': safe_LL},
            'extraction',
            extraction_positions
        )

        return DWTSteganographyService.bits_to_text(''.join(message_bits))
