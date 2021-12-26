
import numpy as np

def simple_demosaic(raw_array, pattern):
  """
  簡易デモザイク処理を行う。
  Parameters
  ----------
  raw_array: numpy array
    入力BayerRAW画像データ
  pattern: int[2, 2]
    Bayerパターン 0:red, 1:green, 2: blue, 3:green

  Returns
  -------
  dms_img: numpy array
  出 力RGB画像 サイズは入力の縦横共に1/2"""

  height, width = raw_array.shape
  dms_img = np.zeros((height // 2, width // 2, 3))
  pattern[pattern == 3] = 1
  dms_img[:, :, pattern[0, 0]] = raw_array[0::2, 0::2]
  dms_img[:, :, pattern[0, 1]] = raw_array[0::2, 1::2]
  dms_img[:, :, pattern[1, 0]] = raw_array[1::2, 0::2]
  dms_img[:, :, pattern[1, 1]] = raw_array[1::2, 1::2]
  return dms_img
