
import numpy as np
import cv2
from scipy.interpolate import UnivariateSpline

def _create_LUT_BUC1(x, y):
    spl = UnivariateSpline(x, y)
    return spl(range(256))


def create_loopup_tables():
    incr_ch_lut = _create_LUT_BUC1(
        [0, 64, 128, 192, 256], [0, 70, 140, 210, 256])
    decr_ch_lut = _create_LUT_BUC1(
        [0, 64, 128, 192, 256], [0, 30, 80, 120, 192])

    return incr_ch_lut, decr_ch_lut


def _warming(orig):
    incr_ch_lut, decr_ch_lut = _create_loopup_tables()

    c_b, c_g, c_r = cv2.split(orig)
    c_r = cv2.LUT(c_r, incr_ch_lut).astype(np.uint8)
    c_b = cv2.LUT(c_b, decr_ch_lut).astype(np.uint8)
    img = cv2.merge((c_b, c_g, c_r))

    H, S, V = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))
    S = cv2.LUT(S, incr_ch_lut).astype(np.uint8)

    output = cv2.cvtColor(cv2.merge((H, S, V)), cv2.COLOR_HSV2BGR)
    return output

def warming(img_handler):
    output = _warming(img_handler)
    return output

def _cooling(orig):
    incr_ch_lut, decr_ch_lut = _create_loopup_tables()

    c_b, c_g, c_r = cv2.split(orig)
    c_r = cv2.LUT(c_r, decr_ch_lut).astype(np.uint8)
    c_b = cv2.LUT(c_b, incr_ch_lut).astype(np.uint8)
    img = cv2.merge((c_b, c_g, c_r))

    H, S, V = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))
    S = cv2.LUT(S, decr_ch_lut).astype(np.uint8)

    output = cv2.cvtColor(cv2.merge((H, S, V)), cv2.COLOR_HSV2BGR)
    return output

def cooling(img_handler):
    output = _cooling(img_handler)
    return output