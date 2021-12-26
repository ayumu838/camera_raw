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

def white_balance(raw_array, wb_gain, raw_colors):
  """
  ホワイトバランスの補正を行う

  Parameters
  ----------
  raw_array: numpy_array
    入力 BayerRAW画像データ
  wb_gain: float[4]
    ホワイトバランスゲイン
  raw_colors: int[h, w]
    RAW画像のカラーチャンネルマトリクス

  Returns
  -------
  wb_img: numpy_array
    出力RAW画像
  """
  norm = wb_gain[1]
  gain_matrix = np.zeros(raw_array.shape)
  for color in (0, 1, 2, 3):
    gain_matrix[raw_colors == color] = wb_gain[color] / norm
  wb_img = raw_array * gain_matrix
  return wb_img

def black_level_correction(raw_array, blc, pattern):
  """
  ブラックレベルの補正処理を行う

  Parameters
  ---------
  raw_array: numpy array
    入力BayerRAM画像データ
  blc: float[4]
    各カラーチャンネルごとのブラックレベル
  pattern: int[2, 2]
    ベイヤーパターン 0:red, 1:green, 2:blue, 3:green

  Returns
  -------
  blc_raw: numpy array
    出力RAW画像
  """
  blc_raw = raw_array.astype('int')
  blc_raw[0::2, 0::2] -= blc[pattern[0, 0]]
  blc_raw[0::2, 1::2] -= blc[pattern[0, 1]]
  blc_raw[1::2, 0::2] -= blc[pattern[1, 0]]
  blc_raw[1::2, 1::2] -= blc[pattern[1, 1]]

  return blc_raw

def gamma_correction(input_img, gamma):
  """
  ガンマ補正処理を行う

  Parameters
  ---------
  input_img: numpy array [h, w, 3]
    入力RGB画像データ
  gamma: float
    ガンマ補正値 通常は2.2

  Returns
  ------
  gamma_img: numpy array[h, w, 3]
    出力RGB画像
  """
  gamma_img = input_img.copy()
  gamma_img[gamma_img < 0] = 0
  gamma_img[gamma_img > 1] = 1.0

  gamma_img = np.power(gamma_img, 1/gamma)
  return gamma_img
