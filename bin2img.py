#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Tool to transform any binary file to a PNG image

Syntax:
bin2img.py <directory>
bin2img.py <inputfile> <outputfile>
"""


import sys
import math
import os

# pip install Pillow
from PIL import (
    Image,
    ImageDraw,
)


class FileData:
    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile


def determine_size(data):
    size = int(math.sqrt(len(data)) + 1)
    return size, size


def getcolor(byteval):
    return (
        ((byteval & 0o300) >> 6) * 64,
        ((byteval & 0o070) >> 3) * 32,
        (byteval & 0o007) * 32,
    )


def bin2img(data):
    xsize, ysize = size = determine_size(data)
    img = Image.new("RGB", size)
    draw = ImageDraw.Draw(img)
    try:
        i = 0
        for y in range(ysize):
            for x in range(xsize):
                draw.point((x, y), fill=getcolor(data[i]))
                i += 1
    except IndexError:
        pass
    return img


def error(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)


def parse_cmdargs(args):
    if len(args) == 2:
        dir = args[1]
        if not os.path.isdir(dir):
            error(f'Given argument "{dir}" must be a directory')

        filepaths = [
            os.path.join(dir, file)
            for file in os.listdir(dir)
            if os.path.isfile(os.path.join(dir, file))
        ]
        if not filepaths:
            error(f'Given directory "{dir}" must contain files')

        files = []
        for file in filepaths:
            outdir = os.path.join(os.path.dirname(args[0]), "output")
            if not os.path.exists(outdir):
                os.mkdir(outdir)
            outfile = os.path.join(outdir, f"{os.path.basename(file)}.png")
            files.append(FileData(file, outfile))

        return files

    elif len(args) == 3:
        infile = args[1]
        outfile = args[2]

        if not os.path.isfile(infile):
            error(f'First argument "{infile}" is not a file')
        if os.path.exists(outfile):
            error(f'File "{outfile}" exists already')

        return [FileData(infile, outfile)]

    else:
        error(__doc__)


def generate_image(infile):
    with open(infile, "rb") as f:
        data = f.read()
    return bin2img(data)


def main(args):
    files = parse_cmdargs(args)
    for file in files:
        infile = file.infile
        outfile = file.outfile

        img = generate_image(infile)
        print(f'Image generated from "{infile}"')

        img.save(outfile, "PNG", compress_level=9)
        print(f'Image stored at "{outfile}"')


if __name__ == "__main__":
    main(sys.argv)
