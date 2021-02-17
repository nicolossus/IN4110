## Exercise 4.1 Grayscale Image Filter and Time Profiling

#### Comments :cookie:

The exercise text first states that we should write a function `grayscale_filter`, followed by that we should write a function `python_color2gray`. At least in how I interpret the instructions on how to implement the functions, these would be indistinguishable. I have therefore only implemented the latter.

#### Contents :shipit:

* [python_color2gray.py](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/grayscale_filter/python_color2gray.py) - pure Python implementation of grayscale filter.

* [numpy_color2gray.py](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/grayscale_filter/numpy_color2gray.py) - vectorized NumPy implementation of grayscale filter.

* [numba_color2gray.py](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/grayscale_filter/numba_color2gray.py) - automatic parallelization, enabled by Numba, implementation of grayscale filter.

* [cython_color2gray_cdef.pyx](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/grayscale_filter/cython_color2gray_cdef.pyx) - Cython implementation of grayscale filter using a combination of `def` and `cdef`.

* [cython_color2gray_cpdef.pyx](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/grayscale_filter/cython_color2gray_cpdef.pyx) - Cython implementation of grayscale filter using `cpdef`.

* [setup.py](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/grayscale_filter/setup.py) - compile instructions for Cython implementations.

* [benchmark_cython_color2gray.py](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/grayscale_filter/benchmark_cython_color2gray.py) - program for benchmarking time usage of Cython implementations.

* [reports](https://github.uio.no/IN3110/IN3110-nicoha/tree/master/assignment4/grayscale_filter/reports) - directory with time profiling reports.

#### Compilation and Usage :moyai:

`cd` into `grayscale_filter` directory.

**Compile Cython Programs:**

    $ python3 setup.py build_ext --inplace

**Run individual .py programs:**

    $ python <filename>.py

This will generate time profiling reports for functions specified by the particular program.

**Generate all time profiling reports:**

    $ bash run.sh
