import numpy as np

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
