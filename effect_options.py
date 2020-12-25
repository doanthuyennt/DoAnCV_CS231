from skimage.util import random_noise
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter
import numpy as np

import streamlit as st


class Effects:

    def __init__(self, image) -> None:
        super().__init__()
 
        self.image = image

    def enhance(self, **kwargs):
        pass

class Grain(Effects):
    def effect(self, **kwargs) -> Image:
        image_array = np.asarray(self.image)
        mode   = st.sidebar.selectbox("Option",['gaussian','localvar','s&p','speckle'])
        
        if mode == 's&p':
            amount = st.sidebar.slider('Grain', min_value = 0.,max_value =  0.3, value = 0.05, step = 0.05)
            noise = random_noise(image_array, mode=mode, amount=amount)
        else:
            noise = random_noise(image_array, mode=mode)
        noise = np.array(255 * noise, dtype=np.uint8)
        return Image.fromarray(noise)
    
class Feather(Effects):
    def effect(self, **kwargs) -> Image:
        

        # Paste image on white background
        RADIUS = st.sidebar.slider('Grain', min_value = 10,max_value =  20, value = 10, step = 2)

        diam = 2*RADIUS
        back = Image.new('RGB', (self.image.size[0]+diam, self.image.size[1]+diam), (255,255,255))
        back.paste(self.image, (RADIUS, RADIUS))

        # Create paste mask
        mask = Image.new('L', back.size, 0)
        draw = ImageDraw.Draw(mask)
        x0, y0 = 0, 0
        x1, y1 = back.size
        for d in range(diam+RADIUS):
            x1, y1 = x1-1, y1-1
            alpha = 255 if d<RADIUS else int(255*(diam+RADIUS-d)/diam)
            draw.rectangle([x0, y0, x1, y1], outline=alpha)
            x0, y0 = x0+1, y0+1

        blur = back.filter(ImageFilter.GaussianBlur(RADIUS/2))
        back.paste(blur, mask=mask)
        
        return back


