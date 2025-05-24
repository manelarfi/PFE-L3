import cv2
import numpy as np
import matplotlib.pyplot as plt

# Haar wavelet filters
sqrt2 = np.sqrt(2)
LOW_PASS_FILTER = [1 / sqrt2, 1 / sqrt2]
HIGH_PASS_FILTER = [-1 / sqrt2, 1 / sqrt2]

def convolve_and_downsample(signal, filt):
    filt_len = len(filt)
    signal_len = len(signal)
    pad_width = filt_len - 1
    padded = np.pad(signal, (pad_width // 2, pad_width // 2), mode='symmetric')
    result = []
    for i in range(0, signal_len, 2):
        val = 0
        for j in range(filt_len):
            val += padded[i + j] * filt[j]
        result.append(val)
    return result

def dwt1d(signal):
    approx = convolve_and_downsample(signal, LOW_PASS_FILTER)
    detail = convolve_and_downsample(signal, HIGH_PASS_FILTER)
    return approx, detail

def dwt2d(image):
    rows, cols = image.shape
    row_transformed = []
    for row in image:
        a, d = dwt1d(row)
        row_transformed.append((a, d))
    
    a_rows = np.array([pair[0] for pair in row_transformed])
    d_rows = np.array([pair[1] for pair in row_transformed])

    a_cols = []
    d_cols = []
    for col in a_rows.T:
        a, d = dwt1d(col)
        a_cols.append(a)
        d_cols.append(d)
    cA = np.array(a_cols).T
    cV = np.array(d_cols).T

    a_cols = []
    d_cols = []
    for col in d_rows.T:
        a, d = dwt1d(col)
        a_cols.append(a)
        d_cols.append(d)
    cH = np.array(a_cols).T
    cD = np.array(d_cols).T

    return cA, cH, cV, cD

def process_and_show(channel, title_prefix):
    cA, cH, cV, cD = dwt2d(channel)

    plt.figure(figsize=(10, 10))
    plt.subplot(2, 2, 1)
    plt.imshow(cA, cmap='gray')
    plt.title(f'{title_prefix} - Approximation (LL)')

    plt.subplot(2, 2, 2)
    plt.imshow(cH, cmap='gray')
    plt.title(f'{title_prefix} - Horizontal (HL)')

    plt.subplot(2, 2, 3)
    plt.imshow(cV, cmap='gray')
    plt.title(f'{title_prefix} - Vertical (LH)')

    plt.subplot(2, 2, 4)
    plt.imshow(cD, cmap='gray')
    plt.title(f'{title_prefix} - Diagonal (HH)')

    plt.tight_layout()
    plt.show()

# ==== Main Execution ====
if __name__ == "__main__":
    image_path = "/home/mananou/Downloads/test.JPG"
    bgr_image = cv2.imread(image_path)

    if bgr_image is None:
        print("Error: Image not found.")
        exit(1)

    # Resize for easier visualization
    bgr_image = cv2.resize(bgr_image, (256, 256))

    # Convert to YCrCb
    ycrcb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2YCrCb)
    Y, Cr, Cb = cv2.split(ycrcb_image)

    # Apply DWT and show each component
    process_and_show(Y, "Y Channel")
    process_and_show(Cr, "Cr Channel")
    process_and_show(Cb, "Cb Channel")
