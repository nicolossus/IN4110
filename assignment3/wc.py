#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys


def wc(*args):
    """
    Count content of one or more files.

    When called with a filename as command line argument; prints the single line
    "a b c fn", where
    a is the number of lines in the file,
    b the number of words,
    c the number of characters, and
    fn the filename.

    Parameters
    ----------
    *args : str, bytes or os.PathLike object
        filename(s)
    """

    for filename in args:
        # Check if filename is an existing regular file
        if os.path.isfile(filename):
            _, file_extension = os.path.splitext(filename)
            if file_extension == ".pdf":
                file_encoding = "ISO-8859-1"
            else:
                file_encoding = "utf-8"
            with open(filename, encoding=file_encoding) as f:
                data = f.read()
                a = len(data.splitlines())
                b = sum(len(line.split()) for line in data.splitlines())
                c = len(data)
            print(a, b, c, filename)
        else:
            print(f"{filename} skipped as it either not exists or is non-regular")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Parameter required: filename | * | *.<file extension>")
        sys.exit()
    else:
        wc(*sys.argv[1:])
