import os, sys

# from PIL import Image
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimpg


def main(argv):
    filename = ''
    up = 2 

    # Make sure that the argument is correct
    if len(argv) != 3:
        sys.exit('Usage: python upsampling.py <filename> <up_factor>')
    else:
        filename = argv[1]
        up = float(argv[2])

    # Check the up factor given is unacceptable
    # Keep it below 10 for now...
    if (up < 1) or (up > 10):
        sys.exit('Please restrict your up factor to be between 1 and 10')

    # Try to read the image given the file name
    try:
        img = plt.imread(filename)
    except IOError as e:
        sys.exit("I/O error({0}): {1}".format(e.errno, e.strerror))
    except:
        sys.exit("Unexpected error", sys.exc_info()[0])

    sizeIm = img.shape

    # Set up a new image with the up factor (2 = double image size)
    nn_canvas = np.zeros((round(sizeIm[0]*up), round(sizeIm[1]*up), 4))

    # Nearest neighbour - take the nearest pixel and stretch to fill
    ###################
    # Get the the scaling factor the rows and columns after rounding
    upx = float(round(sizeIm[0]*up))/sizeIm[0]
    upy = float(round(sizeIm[1]*up))/sizeIm[1]

    # Iterate through the original pixels and fill in the new canvas
    for (x,y,z), value in np.ndenumerate(img):
        print 'x',round(x*upx),round(x*upx+upx)
        print 'y',round(y*upy),round(y*upy+upy)
        nn_canvas[round(x*upx):round(x*upx+upx),
                  round(y*upy):round(y*upy+upy),z] = value
    ###################
    
    # Bilinear interpolation
    # ???

    # Show the original image and the image after nearest neighbour
    figure(1);imshow(img)
    figure(2);imshow(nn_canvas)
    # Pause it so that it appears when calling from terminal
    pause(10)
    

if __name__ == "__main__":
    sys.exit(main(sys.argv))
