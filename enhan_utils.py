
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