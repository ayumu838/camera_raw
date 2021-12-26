import numpy as np

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
