# -*- coding: utf-8 -*-

import rawpy
import matplotlib.pyplot as plt

import raw_process

raw_file = "chart.jpg"
raw = rawpy.imread(raw_file)
raw_array = raw.raw_image

blc = [66, 66, 66, 66]
pattern = raw.raw_pattern
blc_raw = raw_process.black_level_correction(raw_array, blc, pattern)

gain, colors = raw.camera_whitebalance, raw.raw_colors
wb_img = raw_process.white_balance(blc_raw, gain, colors)
dms_img = raw_process.simple_demosaic(wb_img, pattern)
gmm_img = raw_process.gamma_correction(dms_img/1024, 2.2)

plt.figure(figsize=(8,8))
plt.imshow(gmm_img)
plt.axis('off')
plt.show()
