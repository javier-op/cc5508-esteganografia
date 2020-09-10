import matplotlib.pyplot as plt
import pai_io
import sys

def get_bits_hidden_value(image):
    if len(image.shape) == 2:
        return image[0][0]
    else:
        return image[0][0][0]

def unhide_image(image, bits_hidden):
    return image << (8 - bits_hidden)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SyntaxError('usage: unhide.py [path to image]')
    input_image = pai_io.imread(sys.argv[1])
    bits_hidden = get_bits_hidden_value(input_image)
    output = unhide_image(input_image, bits_hidden)
    plt.imshow(output)
    plt.axis('off')
    plt.show()

