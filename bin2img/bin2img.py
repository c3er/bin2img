#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import math
import os

# pip install Pillow
from PIL import (
    Image,
    ImageDraw,
)


_execinfo = {
    "name": os.path.basename(sys.argv[0]),
    "dir" : os.path.dirname(sys.argv[0]),
}


_helpmsg = """\
Syntax:
{0} <directory>
{0} <inputfile> <outputfile>
""".format(_execinfo["name"])


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


def wait():
    print("Press Enter")
    input()


def error(msg):
    print(msg, file=sys.stderr)
    wait()
    sys.exit(1)


def parse_cmdargs(args):
    if len(args) == 2:
        dir = args[1]
        if not os.path.isdir(dir):
            error('Given argument "{}" must be a directory'.format(dir))

        filepaths = (os.path.join(dir, file) for file in os.listdir(dir))
        files = []
        for file in filepaths:
            if os.path.isfile(file):
                outdir = os.path.join(_execinfo["dir"], "output")
                if not os.path.exists(outdir):
                    os.mkdir(outdir)
                outfile = os.path.join(outdir, os.path.basename(file) + ".png")
                files.append(FileData(file, outfile))
        if not files:
            error('Given directory "{}" must contain files'.format(dir))

        return files

    elif len(args) == 3:
        infile = args[1]
        outfile = args[2]

        inisfile = os.path.isfile(infile)
        outisfile = os.path.isfile(outfile)
        if not inisfile and not outisfile:
            error('Both arguments "{}" and "{}" are not files'.format(infile, outfile))
        if not inisfile:
            error('First argument "{}" is not a file'.format(infile))
        if not outisfile:
            error('Second argument "{}" is not a file'.format(outfile))

        return [FileData(infile, outfile)]

    else:
        error(_helpmsg)


def generate_image(infile):
    with open(infile, "rb") as f:
        data = f.read()
    return bin2img(data)


def main(args):
    try:
        files = parse_cmdargs(args)
        for file in files:
            infile = file.infile
            outfile = file.outfile

            img = generate_image(infile)
            print('Image generated from "{}"'.format(infile))

            img.save(outfile, "PNG", compress_level=9)
            print('Image stored at "{}"'.format(outfile))
    finally:
        wait()


if __name__ == "__main__":
    main(sys.argv)