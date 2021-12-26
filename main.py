# -*- coding: utf-8 -*-

from matplotlib import colors, widgets
import rawpy, imageio
import numpy as np
import matplotlib.pyplot as plt

import demosaic
import white_balance
import black_level
import gamma

raw_file = "chart.jpg"
raw = rawpy.imread(raw_file)

print(raw.sizes)

raw_array = raw.raw_image
h, w = raw_array.shape
print(h, w)

plt.rcParams['font.family'] = 'IPAexGothic'

plt.figure(figsize=(8, 6))
plt.imshow(raw_array, cmap='gray')
plt.axis('off')
plt.title(u"Bayer画像をそのまま表示")
# plt.show()

plt.figure(figsize=(8, 8))
plt.imshow(raw_array[1340:1400, 2640:2700], cmap='gray')
plt.axis('off')
plt.title(u'RAW画像の拡大表示')
# plt.show()

raw_color = np.zeros((h, w, 3))

raw_color[0::2, 0::2, 2] = raw_array[0::2, 0::2]
raw_color[0::2, 1::2, 1] = raw_array[0::2, 1::2]
raw_color[1::2, 0::2, 1] = raw_array[1::2, 0::2]
raw_color[1::2, 1::2, 0] = raw_array[1::2, 1::2]

raw_color[raw_color < 0] = 0
raw_color = raw_color / 1024

plt.figure(figsize=(8, 8))
plt.imshow(raw_color)
plt.axis('off')
plt.title(u'RAW画像の各要素に色を割り当てたもの')
# plt.show()

plt.figure(figsize=(8, 8))
digital_gain = 4
plt.imshow(raw_color[1340:1400, 2640:2700] * digital_gain)
plt.axis('off')
plt.title(u'RAW画像の各要素に色を割り当てたものを拡大表示')
# plt.show()


dms_img = demosaic.simple_demosaic(raw_array, raw.raw_pattern)

dms_img[dms_img < 0] = 0
dms_img /= 1024

plt.figure(figsize=(8, 8))
plt.imshow(dms_img)
plt.axis('off')
plt.title(u' 簡易モザイク')
# plt.show()


gain, colors = raw.camera_whitebalance, raw.raw_colors
wb_img = white_balance.white_balance(raw_array, gain, colors)

dms_img = demosaic.simple_demosaic(wb_img, raw.raw_pattern)
dms_img /= 1024
dms_img[dms_img < 0] = 0
dms_img[dms_img > 1] = 1.0

plt.figure(figsize=(8, 8))
plt.imshow(dms_img)
plt.axis('off')
plt.title(u' ホワイトバランス後の画像')
# plt.show()

# blc = raw.black_level_per_channel
blc = [66, 66, 66, 66]
print(blc)

blc_raw = black_level.black_level_correction(raw_array, blc, raw.raw_pattern)

gain, colors = raw.camera_whitebalance, raw.raw_colors
wb_img = white_balance.white_balance(blc_raw, gain, colors)
dms_img = demosaic.simple_demosaic(wb_img, raw.raw_pattern)

plt.figure(figsize=(8, 8))
dms_img /= 1024
dms_img[dms_img < 0] = 0
dms_img[dms_img > 1] = 1.0

plt.imshow(dms_img)
plt.axis('off')
plt.title(u' ブラックレベル補正後の画像')
# plt.show()

# blc = raw.black_level_per_channel
blc = [66, 66, 66, 66]
pattern = raw.raw_pattern
blc_raw = black_level.black_level_correction(raw_array, blc, pattern)
gain, colors = raw.camera_whitebalance, raw.raw_colors
wb_img = white_balance.white_balance(blc_raw, gain, colors)
dms_img = demosaic.simple_demosaic(wb_img , raw.raw_pattern)

gamma_img = gamma.gamma_correction(dms_img/1024, 2.2)

plt.figure(figsize=(8, 8))
plt.imshow(gamma_img)
plt.axis('off')
plt.title(u"ガンマ補正後")
plt.show()
