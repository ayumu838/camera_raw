from matplotlib import image
import rawpy, imageio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image

from raw_process import (
                          simple_demosaic,
                          white_balance,
                          black_level_correction,
                          gamma_correction,
                          demosaic
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

dms_img = demosaic(raw_array, colors)

gmm_full_img = gamma_correction(dms_img / white_level, 2.2)


plt.figure(figsize=(16, 8))

plt.imshow(gmm_full_img)
plt.axis('off')
plt.title("線形補間デモザイク結果")
plt.show()
