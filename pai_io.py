'''
Created on Aug 1, 2019

@author: jsaavedr
io functions
'''
import skimage.io as skio
import numpy as np
import utils

def imread(filename, as_gray = False):
    image = skio.imread(filename, as_gray = as_gray)
    if image.dtype == np.float64 :
        image = utils.to_uint8(image)
    return image
