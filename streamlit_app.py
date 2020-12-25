import numpy as np
import os
import pickle
import streamlit as st
import sys
import urllib
from PIL import Image

import enhancement_options
from enhancement_names import *

import filter_options
from filter_names import *

import effect_options
from effect_names import *

import cv2

def call_filter(filter_choose,image_in):
    f = getattr(filter_options, FILTERS[filter_choose])(image_in)
    return f

def call_enhancer(enhancer_choose,image_in):
    eh = getattr(enhancement_options, ENHANCERS[enhancer_choose])(image_in)
    return eh

def call_effect(effect_choose,image_in):
    ef = getattr(effect_options, EFFECTS[effect_choose])(image_in)
    return ef

def show_image_option(image_in,image_out):
    view_option = st.sidebar.selectbox("Show Image Option",["Side by Side","Split"])
    if  view_option == "Side by Side":
        image_out = Image.fromarray(np.asarray(image_out))
        images   =  [image_in,image_out]
        widths, heights = zip(*(i.size for i in images))
        x_offset = 0
        total_width = sum(widths)
        max_height = max(heights)
        new_im = Image.new('RGB', (total_width, max_height))

        for im in images:
            new_im.paste(im, (x_offset,0))
            x_offset += im.size[0]

        st.image(new_im, use_column_width=True)
    else:
        st.image(image_in, use_column_width=True)
        image_out = Image.fromarray(np.asarray(image_out))
        st.image(image_out, use_column_width=True)

IMAGE_STACK = []

sidebar_op        = st.sidebar.selectbox('',['Show Filter options','Show Enhancement options','Show Effect options'])
filter_names      = list(FILTERS.keys()) 
enhancement_names = list(ENHANCERS.keys()) 
effect_names      = list(EFFECTS.keys())


def image_handling(image_in):
    params = {}
    if sidebar_op == 'Show Filter options':
        st.sidebar.write(
            """Using alot of filter options.
            """
        ) 
        filter_choose = st.sidebar.selectbox("Option",filter_names)
        if filter_choose == 'gaussian_blur':
            radius = st.sidebar.slider(filter_choose, min_value = 2,max_value =  5, value = None, step = 1)
            params['radius'] = radius
        if filter_choose in ['max','min','median','mode']:
            size = st.sidebar.slider(filter_choose, min_value = 3,max_value =  7, value = None, step = 2)
            params['size'] = size

        f = call_filter(filter_choose,image_in)
        image_out = f.filter(**params)

    if sidebar_op == 'Show Enhancement options':
        enhan_choose = st.sidebar.selectbox("Option",enhancement_names)

        if enhan_choose not in ['warm','cool','sepia','saturate']:
            params['factor'] = st.sidebar.slider(enhan_choose, min_value = 1.2,max_value =  2., value = None, step = 0.1)
            eh = call_enhancer(enhan_choose,image_in)
            image_out = eh.enhance(**params)
        if enhan_choose in ['warm','cool']:
            image_in  = cv2.imread('image/USE_THIS.jpg')
            eh = call_enhancer(enhan_choose,image_in)
            image_out = eh.enhance(**params)
            image_in  = Image.open('image/USE_THIS.jpg')
        if enhan_choose in ['sepia','saturate']:
            params['amount'] = st.sidebar.slider(enhan_choose, min_value = 0.,max_value =  1., value = 1., step = 0.05)
            eh = call_enhancer(enhan_choose,image_in)
            image_out = eh.enhance(**params)

    if sidebar_op == 'Show Effect options':
        effect_choose = st.sidebar.selectbox("Option",effect_names)
        ef = call_effect(effect_choose,image_in)
        image_out = ef.effect(**params)

    show_image_option(image_in,image_out)


def main():

    st.title("Image Filtering")

    st.sidebar.title('Features')

    UPLOADED_IMAGE = st.file_uploader(
        label='', type=['jpg', 'png', 'jpeg'])
    showfile = st.empty()

    if not UPLOADED_IMAGE:
        showfile.info('Please upload image file')
        st.stop()
    if UPLOADED_IMAGE:
        IMAGE = Image.open(UPLOADED_IMAGE)
        IMAGE = IMAGE.convert('RGB')
        IMAGE.save('image/USE_THIS.jpg')

    image_in = IMAGE
    image_handling(image_in)
    # revert = st.sidebar.button("Revert")
    # if revert:
    #     image_out = IMAGE    
    
    # image_out = image_in


if __name__ == "__main__":
    main()
