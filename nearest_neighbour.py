import os, sys

# from PIL import Image
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimpg


def main(argv):
    filename = ''
    up = 2 # TODO: Make sure it's not less than zero

    # Make sure that the argument is correct
    if len(argv) != 2:
        sys.exit('Usage: python nearest_neighbour.py <filename>')
    else:
        filename = argv[1]

    # Try to read the image given the file name
    try:
        img = plt.imread(filename)
    except IOError as e:
        sys.exit("I/O error({0}): {1}".format(e.errno, e.strerror))
    except:
        sys.exit("Unexpected error", sys.exc_info()[0])

    sizeIm = img.shape

    # Set up a new image with the up factor (2 = double image size)
    canvas = np.zeros((sizeIm[0]*up, sizeIm[1]*up, 4))

    # Nearest neighbour - simply take the nearest pixel and stretch to fill
    # empty pixel spaces
    for (x,y,z), value in np.ndenumerate(img):
        canvas[x*up:x*up+up,y*up:y*up+up,z] = value

    figure(1);imshow(img)
    figure(2);imshow(canvas)
    pause(10)
    

if __name__ == "__main__":
    sys.exit(main(sys.argv))
