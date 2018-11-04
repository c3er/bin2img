#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Tool to transform any binary file to a PNG image

Syntax:
bin2img.py <file or directory>
bin2img.py <input file or directory> <output file or directory>

If only a file is given, an image file named <file name>.png will be generated
in the same directory as the file.

If the only argument is a directory, all the files in this directory will be
transformed in a directory named <directory name>_images alongside the given
input directory.

Behavior with two arguments is similar but with user determined output path.
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
    img = Image.new("RGB", size, color=(255, 255, 255, 0))
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


def build_dirpaths(indir, outdir):
    file_inputs = [
        os.path.join(indir, file)
        for file in os.listdir(indir)
        if os.path.isfile(os.path.join(indir, file))
    ]
    if not file_inputs:
        error(f'Given directory "{indir}" must contain files')
    os.makedirs(outdir, exist_ok=True)
    files = [
        FileData(file, os.path.join(outdir, f"{os.path.basename(file)}.png"))
        for file in file_inputs
    ]
    return files


def parse_cmdargs(args):
    if len(args) >= 2:
        input = args[1].strip()
        if not os.path.exists(input):
            error(f'File or directory "{input}" does not exist')
        if not os.path.isdir(input) and not os.path.isfile(input):
            error(f'"{input}" could neither be recognized as file nor as directory')

    if len(args) == 2:
        if os.path.isdir(input):
            if input[-1] in ("/", "\\"):
                input = input[:-1]
            outdir = os.path.join(
                os.path.dirname(input),
                f"{os.path.basename(input)}_images")
            return build_dirpaths(input, outdir)
        else:
            outfile = os.path.join(
                os.path.dirname(input),
                f"{os.path.basename(input)}.png")
            return [FileData(input, outfile)]

    elif len(args) == 3:
        output = args[2]

        if os.path.exists(output):
            if os.path.isdir(input) and not os.path.isdir(output):
                error(f'Input "{input}" is a directory but not output "{output}"')
            elif os.path.isfile(input) and not os.path.isfile(output):
                error(f'Input "{input}" is a file but not output "{output}"')

        if os.path.isdir(input):
            return build_dirpaths(input, output)
        else:
            return [FileData(input, output)]
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
