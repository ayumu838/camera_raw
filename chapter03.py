from matplotlib import image
import rawpy, imageio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image

from raw_process import (
                          simple_demosaic,
                          white_balance,
                          black_level_correction,
                          gamma_correction
                        )

plt.rcParams["font.family"] = "IPAexGothic"

raw_file = "chart.jpg"
raw = rawpy.imread(raw_file)
raw_array = raw.raw_image
h, w = raw_array.shape

# blc = raw.black_level_per_channel
blc = [66, 66, 66, 66]
pattern = raw.raw_pattern
blc_raw = black_level_correction(raw_array, blc, pattern)

gains, colors = raw.camera_whitebalance, raw.raw_colors
wb_raw = white_balance(blc_raw, gains, colors)

dms_img = simple_demosaic(wb_raw, pattern)
white_level = 1024.0

dms_img = dms_img / white_level

gmm_img = gamma_correction(dms_img, 2.2)

plt.figure(figsize=(16, 8))
plt.imshow(gmm_img)
plt.axis("off")
plt.title("簡易デモザイクを使ったRAW現像結果")
# plt.show()

jpg_img = image.imread("chart.jpg")
jpg_img = jpg_img / jpg_img.max()
h2, w2, c = jpg_img.shape

two_img = np.zeros((h2, w2*2, c))
two_img[0:, w2:, :] = jpg_img
two_img[h//4:h//4+h//2, w//4:w//4+w//2, :] = gmm_img

plt.figure(figsize=(16, 8))
plt.imshow(two_img)
plt.axis("off")
plt.title("簡易RAW現像結果(左), JPEG画像(右)")
plt.show()
