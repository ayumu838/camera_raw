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

jpg_img = image.imread("chart.jpg")
jpg_img = jpg_img / jpg_img.max()
h2, w2, c = jpg_img.shape


plt.figure(figsize=(16, 8))
plt.subplot(1, 2, 1)
y1, x1 = 740, 835
dy1, dx1 = 100, 100
plt.imshow(gmm_img[y1:y1+dy1, x1:x1+dx1])
plt.axis("off")
plt.title(u"簡易デモザイク結果")

plt.subplot(1, 2, 2)
y2, x2 = y1 * 2, x1 * 2
dy2, dx2 = dy1 * 2, dx1 * 2
plt.imshow(jpg_img[y2:y2+dy2, x2:x2+dx2])
plt.axis("off")
plt.title(u"JPEG画像")

plt.show()
