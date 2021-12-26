# -*- coding: utf-8 -*-

import rawpy, imageio
import numpy as np
import matplotlib.pyplot as plt

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

pattern = raw.raw_pattern
pattern[pattern == 3] = 1
print(pattern)

dms_img = np.zeros((h//2, w//2, 3))
for y in range(0, h, 2):
  for x in range(0, w, 2):
    dms_img[y // 2, x //2, pattern[0, 0]] += raw_array[y + 0, x + 0]
    dms_img[y // 2, x //2, pattern[0, 1]] += raw_array[y + 0, x + 1]
    dms_img[y // 2, x //2, pattern[1, 0]] += raw_array[y + 1, x + 0]
    dms_img[y // 2, x //2, pattern[1, 1]] += raw_array[y + 1, x + 1]
    dms_img[y // 2, x // 2, 1] /= 2

dms_img[dms_img < 0] = 0
dms_img /= 1024

plt.figure(figsize=(8, 8))
plt.imshow(dms_img)
plt.axis('off')
plt.title(u' 簡易モザイク')
plt.show()
