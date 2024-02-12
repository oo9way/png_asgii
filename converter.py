import sys
import argparse
import time

import numpy as np
from PIL import Image

from colors import colors

# 70 levels of gray
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# 10 levels of gray
gscale2 = '@%#*+=-:. '


def getAverageL(image):
    """
    Given PIL Image, return average value of grayscale value
    """
    # get image as numpy array
    im = np.array(image)

    # get shape
    w, h = im.shape

    # get average
    return np.average(im.reshape(w * h))


def covertImageToAscii(file_name, cols, scale, more_levels):
    """
    Given Image and dims (rows, cols) returns an m*n list of Images
    """
    # declare globals
    global gscale1, gscale2

    # open image and convert to grayscale
    image = Image.open(file_name).convert('L')

    # store dimensions
    W, H = image.size[0], image.size[1]

    # compute width of tile
    w = W / cols

    # compute tile height based on aspect ratio and scale
    h = w / scale

    # compute number of rows
    rows = int(H / h)

    # check if image size is too small
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)

    # ascii image is a list of character strings
    ascii_image = []

    # generate list of dimensions
    for j in range(rows):
        y1 = int(j * h)
        y2 = int((j + 1) * h)

        # correct last tile
        if j == rows - 1:
            y2 = H

        # append an empty string
        ascii_image.append("")

        for i in range(cols):

            # crop image to tile
            x1 = int(i * w)
            x2 = int((i + 1) * w)

            # correct last tile
            if i == cols - 1:
                x2 = W

            # crop image to extract tile
            img = image.crop((x1, y1, x2, y2))

            # get average luminance
            avg = int(getAverageL(img))

            # look up ascii char
            if more_levels:
                gsval = gscale1[int((avg * 69) / 255)]
            else:
                gsval = gscale2[int((avg * 9) / 255)]

            # append ascii char to string
            ascii_image[j] += gsval

    # return txt image
    return ascii_image


# main() function
def main():
    # create parser
    descStr = "This program converts an image into ASCII art."
    parser = argparse.ArgumentParser(description=descStr)
    # add expected arguments
    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='scale', required=False)
    parser.add_argument('--out', dest='outFile', required=False)
    parser.add_argument('--cols', dest='cols', required=False)
    parser.add_argument('--morelevels', dest='more_levels', action='store_true')
    parser.add_argument('--title', dest='title', required=False)
    parser.add_argument('--font', dest='font', required=False)
    parser.add_argument('--background', dest='background', required=False)

    # parse args
    args = parser.parse_args()

    imgFile = args.imgFile

    # set output file
    outFile = 'out.txt'
    if args.outFile:
        outFile = args.outFile

    # set scale default as 0.43 which suits
    # a Courier font
    scale = 0.43
    if args.scale:
        scale = float(args.scale)

    # set cols
    cols = 80
    if args.cols:
        cols = int(args.cols)

    if args.font:
        font_color = colors[str(args.font).lower()]
        sys.stdout.write(font_color)

    if args.title:
        print(args.title)

    # convert image to ascii txt
    ascii_image = covertImageToAscii(imgFile, cols, scale, args.more_levels)

    for row in ascii_image:
        time.sleep(0.2)
        sys.stdout.write(row + '\n')

    sys.stdout.write(colors['end'])


# call main
if __name__ == '__main__':
    main()
