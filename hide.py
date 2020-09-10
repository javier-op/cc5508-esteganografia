import matplotlib.pyplot as plt
import numpy as np
import pai_io
import sys

def hide_image(image_A, image_B, bits_len):
    image_A = (image_A >> bits_len) << bits_len
    image_B = image_B >> (8 - bits_len)
    return image_A | image_B

def match_images_dimensions(image_A, image_B):
    if len(image_A.shape) > len(image_B.shape):
        image_B = np.stack((image_B,)*image_A.shape[2], axis=-1)
    if len(image_B.shape) > len(image_A.shape):
        image_A = np.stack((image_A,)*image_B.shape[2], axis=-1)
    template = np.zeros(image_A.shape, dtype=np.uint8)
    min_y = min(image_A.shape[0], image_B.shape[0])
    min_x = min(image_A.shape[1], image_B.shape[1])
    template[:min_y, :min_x] = image_B[:min_y, :min_x]
    image_B = template
    return image_A, image_B

def set_bits_hidden_value(image, bits_hidden):
    bits_hidden = np.uint8(bits_hidden)
    if len(output.shape) == 2:
        output[0][0] = bits_hidden
    else:
        output[0][0][0] = bits_hidden
    return output

if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise SyntaxError('Correct usage -> hide.py [path to image A] [path to image B] [number of bits to hide]')
    try:
        int(sys.argv[3])
    except:
        raise ValueError('Number of bits must be an integer between 0 and 8')
    if int(sys.argv[3]) > 8:
        raise ValueError('Number of bits to hide cannot be higher than 8')
    image_A = pai_io.imread(sys.argv[1])
    image_B = pai_io.imread(sys.argv[2])
    image_A, image_B = match_images_dimensions(image_A, image_B)
    output = hide_image(image_A, image_B, int(sys.argv[3]))
    output = set_bits_hidden_value(output, int(sys.argv[3]))
    plt.imshow(output)
    plt.axis('off')
    plt.show()
