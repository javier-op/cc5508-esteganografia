import argparse
import matplotlib.pyplot as plt
import numpy as np
import pai_io

def hide_image(image_A, image_B, bits_hidden, image_B_disp):
    image_A = (image_A >> bits_hidden) << bits_hidden
    image_B = image_B >> image_B_disp
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

def get_max_bit_size(image):
    max_val = np.amax(image)
    return int(np.ceil(np.log2(max_val+1)))

def set_bits_hidden_value(image, bits_hidden):
    if len(image.shape) == 2:
        image[0][0] = bits_hidden
    else:
        image[0][0][0] = bits_hidden
    return image

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hide an image inside another.')
    parser.add_argument('-imageA', type=str, help='Image that hides another', required=True)
    parser.add_argument('-imageB', type=str, help='Image that is hidden', required=True)
    parser.add_argument('-b', type=np.uint8, help='Amount of bits to hide')
    args = parser.parse_args()
    image_A = pai_io.imread(args.imageA)
    image_B = pai_io.imread(args.imageB)
    image_A, image_B = match_images_dimensions(image_A, image_B)
    output = None
    bits_to_hide = args.b
    if bits_to_hide is None:
        max_capacity = int(np.ceil(get_max_bit_size(image_A) * 3.0 / 8.0))
        bits_to_hide = get_max_bit_size(image_B)
        if bits_to_hide > max_capacity:
            raise ValueError("imageB size exceeds imageA's capacity to hide")
        output = hide_image(image_A, image_B, bits_to_hide, 0)
    else:
        max_b_size = get_max_bit_size(image_B)
        if bits_to_hide > max_b_size:
            raise ValueError("b parameter larger than imageB's most significant bit")
        output = hide_image(image_A, image_B, bits_to_hide, max_b_size-bits_to_hide)
    output = set_bits_hidden_value(output, bits_to_hide)
    pai_io.imsave('hidden.png', output)
    plt.imshow(output)
    plt.axis('off')
    plt.show()
