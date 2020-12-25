from PIL import Image,ImageEnhance
from enhancement_names import *
from enhan_utils import create_loopup_tables
import cv2
import numpy as np
class ImageEnhancer:

    def __init__(self, image) -> None:
        super().__init__()
 
        self.image = image

    def enhance(self, **kwargs):
        pass

class Contrast(ImageEnhancer):
    def enhance(self, **kwargs) -> Image:
        contrast = ImageEnhance.Contrast(self.image)
        if 'factor' in kwargs:
            factor   = kwargs['factor']
        else:
            factor = 1.2
        return contrast.enhance(factor)

class Brightness(ImageEnhancer):
    def enhance(self, **kwargs) -> Image:
        brightess = ImageEnhance.Brightness(self.image)
        if 'factor' in kwargs:
            factor   = kwargs['factor']
        else:
            factor = 1.2
        return brightess.enhance(factor)

class Color(ImageEnhancer):
    def enhance(self, **kwargs) -> Image:
        color = ImageEnhance.Color(self.image)
        if 'factor' in kwargs:
            factor   = kwargs['factor']
        else:
            factor = 1.2
        return color.enhance(factor)

class Warm(ImageEnhancer):
    def __init__(self,image):
        super(Warm, self).__init__(image)
        incr_ch_lut, decr_ch_lut = create_loopup_tables()
        self.incr_ch_lut = incr_ch_lut
        self.decr_ch_lut = decr_ch_lut
    def enhance(self,**kwargs):

        B, G, R = cv2.split(self.image)
        R = cv2.LUT(R, self.incr_ch_lut).astype(np.uint8)
        B = cv2.LUT(B, self.decr_ch_lut).astype(np.uint8)
        img = cv2.merge((B, G, R))

        H, S, V = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))
        S = cv2.LUT(S, self.incr_ch_lut).astype(np.uint8)

        warmed = cv2.cvtColor(cv2.merge((H, S, V)), cv2.COLOR_HSV2RGB)
        warmed = Image.fromarray(warmed)

        return warmed

class Cool(ImageEnhancer):
    def __init__(self,image):
        super(Cool, self).__init__(image)
        incr_ch_lut, decr_ch_lut = create_loopup_tables()
        self.incr_ch_lut = incr_ch_lut
        self.decr_ch_lut = decr_ch_lut

    def enhance(self, **kwargs):

        B, G, R = cv2.split(self.image)
        R = cv2.LUT(R, self.decr_ch_lut).astype(np.uint8)
        B = cv2.LUT(B, self.incr_ch_lut).astype(np.uint8)
        img = cv2.merge((B, G, R))

        H, S, V = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))
        S = cv2.LUT(S, self.decr_ch_lut).astype(np.uint8)

        cooled = cv2.cvtColor(cv2.merge((H, S, V)), cv2.COLOR_HSV2RGB)
        cooled = Image.fromarray(cooled)

        return cooled

class Sepia(ImageEnhancer):
    '''https://www.w3.org/TR/filter-effects-1/#sepiaEquivalent'''
    def enhance(self,**kwargs):
        amount = kwargs['amount']
        # amount = 1.
        SEPIA_TRANS_MATRIX = np.array(
            [[0.393 + 0.607 * (1.- amount),0.769 + 0.607 * (1.- amount),0.189 + 0.607 * (1.- amount)],
            [0.349  - 0.349 * (1.- amount),0.686 + 0.314 * (1.- amount),0.168 + 0.168 * (1.- amount)],
            [0.272  - 0.272 * (1.- amount),0.534 - 0.534 * (1.- amount),0.131 + 0.869 * (1.- amount)]]
        )
        image_np     = np.asarray(self.image)
        image_np_new = np.matmul(image_np,SEPIA_TRANS_MATRIX.T)

        # image_np_new[image_np_new <= 140] = 0
        image_np_new[image_np_new >= 255] = 255
        return Image.fromarray(image_np_new.astype(np.uint8))


class Saturate(ImageEnhancer):
    '''https://www.w3.org/TR/filter-effects-1/#saturateEquivalent'''
    def enhance(self,**kwargs):
        amount = kwargs['amount']
        SATURATE_TRANS_MATRIX = np.array(
            [[0.213 + 0.787 * amount,0.715 - 0.715 * amount,0.072 - 0.072 * amount],
            [0.213  - 0.213 * amount,0.715 + 0.285 * amount,0.072 - 0.072 * amount],
            [0.213  - 0.213 * amount,0.715 - 0.715 * amount,0.072 + 0.928 * amount]]
        )
        image_np     = np.asarray(self.image)
        image_np_new = np.matmul(image_np,SATURATE_TRANS_MATRIX.T)

        # image_np_new[image_np_new <= 140] = 0
        image_np_new[image_np_new >= 255] = 255
        return Image.fromarray(image_np_new.astype(np.uint8))        

