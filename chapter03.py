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

def mirror(x, min, max):
  if x < min:
    return min - x
  elif x >= max:
    return 2 * max - x - 2
  else:
    return x

dms_img = np.zeros((h, w, 3))
bayer_pattern = raw.raw_pattern
for y in range(0, h):
  for x in range(0, w):
    color = bayer_pattern[y % 2, x % 2]
    y0 = mirror(y-1, 0, h)
    y1 = mirror(y+1, 0, h)
    x0 = mirror(x-1, 0, w)
    x1 = mirror(x+1, 0, w)

    # red
    if color == 0:
      dms_img[y, x, 0] = wb_raw[y, x]
      dms_img[y, x, 1] = (wb_raw[y0, x] + wb_raw[y,  x0] + \
                          wb_raw[y, x1] + wb_raw[y1,  x] )/4
      dms_img[y, x, 2] = (wb_raw[y0, x0] + wb_raw[y0,  x1] + \
                          wb_raw[y1, x0] + wb_raw[y1,  x1] )/4
    # green1
    elif color == 1:
      dms_img[y, x, 0] = (wb_raw[y, x0] + wb_raw[y, x1]) / 2
      dms_img[y, x, 1] = wb_raw[y, x]
      dms_img[y, x, 2] = (wb_raw[y0, x] + wb_raw[y1, x]) / 2

    # blue
    elif color == 2:
      dms_img[y, x, 0] = (wb_raw[y0, x0] + wb_raw[y1, x0] + \
                          wb_raw[y0, x1] + wb_raw[y0, x1]) / 4
      dms_img[y, x, 1] = (wb_raw[y0, x] + wb_raw[y1, x] + \
                          wb_raw[y, x0] + wb_raw[y, x1]) / 4
      dms_img[y, x, 2] = (wb_raw[y, x])

    # green2
    else:
      dms_img[y, x, 0] = (wb_raw[y0, x0] + wb_raw[y0, x1]) / 2
      dms_img[y, x, 1] = wb_raw[y, x]
      dms_img[y, x, 2] = (wb_raw[y, x0] + wb_raw[y0, x1]) / 2

gmm_full_img = gamma_correction(dms_img / white_level, 2.2)

plt.figure(figsize=(16, 8))
plt.imshow(gmm_full_img)
plt.axis('off')
plt.show()
