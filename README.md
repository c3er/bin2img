# Binary To Image

Transform any binary file to a PNG image file.

## Prerequisites

Python 3.6 or higher is needed.

Additionally, the library "Pillow" is needed. To install it, type:

```
$ pip3 install -r requirements.txt
```

## Usage

```
$ bin2img.py <file or directory>
```

or

```
$ bin2img.py <input file or directory> <output file or directory>
```

If only a file is given, an image file named `<file name>.png` will be generated
in the same directory as the file.

If the only argument is a directory, all the files in this directory will be
transformed in a directory named `<directory name>_images` alongside the given
input directory.

Behavior with two arguments is similar but with user determined output path.

## Examples

### [Putty](https://www.putty.org/)

![Putty image](examples/putty.exe.png)

### [Sysinternals Process Explorer](https://docs.microsoft.com/en-us/sysinternals/downloads/)

![ProcExp image](examples/procexp.exe.png)

### [Putty](https://www.putty.org/) in shades of Grey

![Putty image](examples/putty.exe_grey.png)

## Notes

[miku](https://github.com/miku) implemented a [similar tool "binpic"](https://github.com/miku/binpic) inspired by this tool and implemented in [the Go language](https://golang.org/)

## Copyright and License

This tool is made by Christian Dreier. If you find a copy somewhere, you find the original at [GitHub](https://github.com/c3er/bin2img).

You can use and copy this tool under the conditions of the MIT license.
