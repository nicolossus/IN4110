# IN4110 Assignment 4

Requested a 3 day extension due to illness.

## Python for Instagram

`instapy` is a package for turning your colorful image of choice into a dramatic grayscale or nostalgic sepia image.

## Structure

#### Exercise 4.0 Profiling Warm-Up

The __[profiling](https://github.uio.no/IN3110/IN3110-nicoha/tree/master/assignment4/profiling)__ directory contains programs that both profile the time usage of functions and generate time profiling reports. For details see the __[grayscale_filter README](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/profiling/README.md)__.

#### Exercise 4.1 Grayscale Filter

The __[grayscale_filter](https://github.uio.no/IN3110/IN3110-nicoha/tree/master/assignment4/grayscale_filter)__ directory contains programs that apply a grayscale image kernel on color images and time profiling reports. For details see the __[grayscale_filter README](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/grayscale_filter/README.md)__.


#### Exercise 4.2 Sepia Filter

The __[sepia_filter](https://github.uio.no/IN3110/IN3110-nicoha/tree/master/assignment4/sepia_filter)__ directory contains programs that apply a sepia image kernel on color images and time profiling reports. For details see the __[sepia_filter README](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/sepia_filter/README.md)__.

#### Exercise 4.3 Develop the `instapy` Package

**Note:** The code for the image filters in the `instapy` package is developed to be more versatile than the code used for benchmarking (Ex. 4.1 and Ex. 4.2). This is by design. Benchmarking a pipeline of loading an image, applying the filter kernel and saving the new image should be sufficient to highlight potential differences between the implementations, and too flexible code could obscure the results.

* [instapy](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/instapy) - directory with package source code
  * [\_\_init\_\_.py](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/instapy/__init__.py) - mark directory as Python package directory
  * [_python.py](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/instapy/_python.py) - pure Python implementation of image filters. Intended for internal use only.
  * [_numpy.py](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/instapy/_numpy.py) - vectorized NumPy implementation of image filters. Intended for internal use only.
  * [_numba.py](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/instapy/_numba.py) - automatic parallelization, enabled by Numba, implementation of image filters. Intended for internal use only.
  * [_cython.pyx](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/instapy/_cython.pyx) - Cython implementation of image filters. Intended for internal use only.
  * [filters.py](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/instapy/filters.py) - functions for the image filters intended for use. Implementation etc. can be specified. See **Usage** below. 
* [setup.py](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/setup.py) - build script for `setuptools`.
* [tests](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/tests) - directory with unit tests for the package

#### Exercise 4.4 User Interface

* [bin](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/bin) - directory with `instapy` command-line interface (CLI) script.

#### Exercise 4.5 Stepless Sepia Filter

The stepless sepia filter is implemented for all methods (Python, NumPy, Numba, Cython) in the [source code](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/instapy) of `instapy`.

## Installation

`cd` into root directory (`assignment4` in this case)

**Development Install**

    $ pip install --editable .

**Install Package**

    $ pip install .


## Tests

`cd` into root directory (`assignment4` in this case)

**Run tests:**

    $ pytest -v -p no:warnings


## Usage

**instapy CLI:**

```
usage: instapy [-h] -f IMAGEFILE [-o OUTFILE] (-g | -se)
               [-i {python,numpy,numba,cython}] [-sc SCALE] [-am SEPIA_AMOUNT]

Turn your colorful image of choice into a dramatic grayscale or nostalgic
sepia image.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --out OUTFILE
                        The output filename. Parameter "auto" autosave the
                        image with applied filter in original filename.
                        (default: auto)
  -i {python,numpy,numba,cython}, --implement {python,numpy,numba,cython}
                        Choose the implementation. (default: numpy)
  -sc SCALE, --scale SCALE
                        Scale factor to resize image. (default: None)
  -am SEPIA_AMOUNT, --amount SEPIA_AMOUNT
                        Amount of sepia effect. 1 is full, 0 nothing.
                        (default: 1)

required arguments:
  -f IMAGEFILE, --file IMAGEFILE
                        The filename of image to apply filter on. (default:
                        None)
  -g, --gray            Select grayscale filter. (default: False)
  -se, --sepia          Select sepia filter. (default: False)
```

**Example usage in Python scripts:**

```Python
from instapy.filters import grayscale_image, sepia_image

imagefile = "rain.jpg"  # Colorful image

## Grayscale Filter

# Default arguments; only returns grayscale image as array
grayscale_img = grayscale_image(
    imagefile, outfile=None, scale=None, method="numpy")
# Equivalent
grayscale_img = grayscale_image(imagefile)

# outfile="auto" autosaves the image with the used filter added to
# original filename, i.e. rain.jpg -> rain_grayscale.jpg
grayscale_img = grayscale_image(
    imagefile, outfile="auto", scale=None, method="numpy")

# New image can also be saved with specified filename
grayscale_img = grayscale_image(
    imagefile, outfile="rain_grayscale.jpg", scale=None, method="numpy")

# Set 'scale' keyword as a fraction to resize image. E.g., scale=0.5
# halves image dimensions whereas scale=2 doubles
grayscale_img = grayscale_image(
    imagefile, outfile="auto", scale=0.5, method="numpy")

# Choose implementation with the 'method' keyword; either "python",
# "numpy", "numba" or "cython"
grayscale_img = grayscale_image(imagefile, method="cython")

## Sepia Filter

# Default arguments; only returns sepia image as array
sepia_image = sepia_image(imagefile, outfile=None,
                          scale=None, sepia_amount=1, method="numpy")
# Equivalent
sepia_image = sepia_image(imagefile)

# Similar usage to 'grayscale_image' with the exception of the
# 'sepia_amount' keyword. Pass values from 0-1 in order to define
# 0-100% amount sepia effect
sepia_image = sepia_image(imagefile, outfile="auto",
                          sepia_amount=0.5, method="numba")

```
