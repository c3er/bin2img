#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math

# pip install Pillow
from PIL import (
    Image,
    ImageDraw,
)


def determine_size(data):
    size = int(math.sqrt(len(data)) + 1)
    return size, size


def getcolor(byteval):
    color = (
        ((byteval & 0xc0) >> 6) * 64,
        ((byteval & 0x38) >> 3) * 32,
        (byteval & 0x07) * 32,
    )
    return color


def bin2img(data):
    xsize, ysize = size = determine_size(data)
    img = Image.new("RGB", size)
    draw = ImageDraw.Draw(img)
    try:
        i = 0
        for y in range(ysize):
            for x in range(xsize):
                color = getcolor(data[i])
                draw.point((x, y), fill=color)
                i += 1
    except IndexError:
        pass
    return img


def parse_cmdargs(args):
    infile = args[1]
    outfile = args[2]
    return infile, outfile


def main(args):
    infile, outfile = parse_cmdargs(args)
    with open(infile, "rb") as f:
        data = f.read()
    print("File read")

    img = bin2img(data)
    print("Image generated")

    img.save(outfile, "PNG", compress_level=9)
    print('Image stored at "{}"'.format(outfile))


if __name__ == "__main__":
    main(sys.argv)