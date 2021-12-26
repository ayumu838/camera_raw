import numpy as np

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
