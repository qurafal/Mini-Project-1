import cv2 
import numpy as np
import matplotlib.pyplot as plt

def MenghitungHistogram(img):
    Histogram = np.zeros((256, 1), np.int32)
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            r = img[i, j]
            Histogram[r] = Histogram[r] + 1
    return Histogram

def hist_match(source, template):
    hist_src = MenghitungHistogram(source)
    hist_tmpl = MenghitungHistogram(template)

    cdf_src = np.cumsum(hist_src)
    cdf_tmpl = np.cumsum(hist_tmpl)

    cdf_src = cdf_src / cdf_src[-1]
    cdf_tmpl = cdf_tmpl / cdf_tmpl[-1]

    mapping = np.zeros(256, dtype=np.uint8)

    j = 0
    for i in range(256):
        while j < 255 and cdf_tmpl[j] < cdf_src[i]:
            j += 1
        mapping[i] = j

    matched = mapping[source]

    return matched

def convolve(image, kernel):
    kh, kw = kernel.shape
    pad_h = kh // 2
    pad_w = kw // 2

    if image.ndim == 2:
        padded = np.pad(image.astype(np.float32), ((pad_h, pad_h), (pad_w, pad_w)), mode="edge")
        windows = np.lib.stride_tricks.sliding_window_view(padded, (kh, kw))
        filtered = np.tensordot(windows, kernel.astype(np.float32), axes=((-2, -1), (0, 1)))
        return np.clip(filtered, 0, 255).astype(np.uint8)

    channels = [convolve(image[:, :, c], kernel) for c in range(image.shape[2])]
    return np.stack(channels, axis=2)

def gauss_kernel(size, sigma):
    half = size // 2
    kernel = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            x, y = j - half, i - half
            kernel[i, j] = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    kernel /= kernel.sum()  
    return kernel

def gauss_filter(image, size, sigma):
    kernel = gauss_kernel(size, sigma)
    return convolve(image, kernel)

def median_filter(image, ksize=3):
    if ksize % 2 == 0:
        raise ValueError("ksize must be odd for median filtering")

    pad = ksize // 2

    if image.ndim == 2:
        padded = np.pad(image, ((pad, pad), (pad, pad)), mode="edge")
        windows = np.lib.stride_tricks.sliding_window_view(padded, (ksize, ksize))
        filtered = np.median(windows, axis=(-2, -1))
        return np.clip(filtered, 0, 255).astype(np.uint8)

    channels = [median_filter(image[:, :, c], ksize) for c in range(image.shape[2])]
    return np.stack(channels, axis=2)
import numpy as np

def laplacian_filter(image):
    kernel = np.array([
        [0, -1, 0],
        [-1, 4, -1],
        [0, -1, 0]
    ])

    lap = convolve(image, kernel)

    # sharpening
    sharp = image.astype(np.int16) - lap.astype(np.int16)

    return np.clip(sharp, 0, 255).astype(np.uint8)

def unsharp_mask(image, sigma=0.5, kernel_size=3, amount=1.0):
    kernel = gauss_kernel(kernel_size, sigma)
    
    blurred = convolve(image, kernel)
    
    mask = image - blurred

    sharpened = image + (amount * mask)

    return np.clip(sharpened, 0, 255).astype(np.uint8)




before = cv2.imread("Input/test_image_lena_noisy.png")
target = cv2.imread("Input/test_image_lena_ori.png")
matched = median_filter(before, 7)
matched = gauss_filter(matched, 7, 3)
matched = unsharp_mask(matched)
matched = laplacian_filter(matched)
matched = hist_match(matched, target)


cv2.imshow("bef",before)
cv2.imshow("target",target)
cv2.imshow("matched",matched)


output_path = "Output/hasil_proses.png"
saved = cv2.imwrite(output_path, matched)

cv2.waitKey(0)
cv2.destroyAllWindows()