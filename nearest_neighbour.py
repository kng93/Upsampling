import os, sys

# from PIL import Image
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimpg


def main(argv):
    filename = ''

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

    imshow(img)
    pause(10)
    

if __name__ == "__main__":
    sys.exit(main(sys.argv))
