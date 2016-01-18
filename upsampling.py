import os, sys

# from PIL import Image
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimpg

# base1, base2 = surrounding pixels from original image
# diff1, diff2 = scaling factors (how close to original pixels)
def lin_interp(cur_p, orig_p, end_p, length, up):
    diff1, diff2, base1, base2  = 0.5, 0.5, -1, -1
        
    # If pixel is at the beginning of the new image, use NN
    if cur_p <= orig_p:
        base1 = 0
    # If pixel is at the end of the new image, use NN
    elif cur_p >= end_p:
        base1 = length-1
    # If pixel is in the middle, do bilinear interpolation
    else:
        # Original x location
        loc = float(cur_p - orig_p)/up
        base1 = np.floor(loc)
        base2 = base1+1

        # Difference between two surrounding x pixels
        diff1 = abs(loc - base1)
        diff2 = abs(base2 - loc)

    base2 = base2 if base2 >= 0 else base1
    return base1, base2, diff1, diff2
    

def main(argv):
    filename = ''
    up = 2 # TODO: Allow to scale differently for x + y

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
    nn_canvas = np.zeros((round(sizeIm[0]*up), round(sizeIm[1]*up), sizeIm[2]))
    nSize = nn_canvas.shape
    
    # Get the the scaling factor the rows and columns after rounding
    upx = float(round(sizeIm[0]*up))/sizeIm[0]
    upy = float(round(sizeIm[1]*up))/sizeIm[1]

    # Show original image
    figure(1);imshow(img)

    # Nearest neighbour - take the nearest pixel and stretch to fill
    ###################
    #Iterate through the original pixels and fill in the new canvas
    for (x,y,z), value in np.ndenumerate(img):
        nn_canvas[round(x*upx):round(x*upx+upx),
                  round(y*upy):round(y*upy+upy),z] = value
    ###################

    # Show the original image and the image after nearest neighbour
    figure(2);imshow(nn_canvas)

    bl_canvas = np.zeros((round(sizeIm[0]*up), round(sizeIm[1]*up), sizeIm[2]))    
    # Bilinear interpolation
    ###################
    # Location of original (0,0) and (x,y) (last) pixel on new canvas
    point00 = (upx/2.0, upy/2.0)
    pointxy = (nSize[0] - upx/2.0, nSize[1] - upy/2.0)
    # Go through the new canvas - each pixel need to be calculated
    for (x,y,z), value in np.ndenumerate(bl_canvas):
        base1x, base2x, base1y, base2y = 0, 0, 0, 0
        diff1x, diff2x, diff1y, diff2y = 0, 0, 0, 0
        
        # FOR X
        base1x, base2x, diff1x, diff2x = lin_interp(x, point00[0], pointxy[0], sizeIm[0], upx)
        base1y, base2y, diff1y, diff2y = lin_interp(y, point00[1], pointxy[1], sizeIm[1], upy)
        
        tmp1 = img[base1x, base1y, z]*diff2x + img[base2x, base1y, z]*diff1x
        tmp2 = img[base1x, base2y, z]*diff2x + img[base2x, base2y, z]*diff1x

        bl_canvas[x,y,z] = tmp1*diff2y + tmp2*diff1y

    figure(3);imshow(bl_canvas)

    
    ###################
    
    # Pause it so that it appears when calling from terminal
    pause(30)
    

if __name__ == "__main__":
    sys.exit(main(sys.argv))
