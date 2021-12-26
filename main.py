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
plt.show()
