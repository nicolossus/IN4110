## Exercise 4.2 Sepia Image Filter and Time Profiling


#### Contents :shipit:

* [python_color2sepia.py](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/sepia_filter/python_color2sepia.py) - pure Python implementation of sepia filter.

* [numpy_color2sepia.py](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/sepia_filter/numpy_color2sepia.py) - vectorized NumPy implementation of sepia filter.

* [numba_color2sepia.py](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/sepia_filter/numba_color2sepia.py) - automatic parallelization, enabled by Numba, implementation of sepia filter.

* [cython_color2sepia.pyx](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/sepia_filter/cython_color2sepia.pyx) - Cython implementation of sepia filter.

* [setup.py](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/sepia_filter/setup.py) - compile instructions for Cython implementation.

* [benchmark_cython_color2sepia.py](https://github.uio.no/IN3110/IN3110-nicoha/blob/master/assignment4/sepia_filter/benchmark_cython_color2sepia.py) - program for benchmarking time usage of Cython implementation.

* [reports](https://github.uio.no/IN3110/IN3110-nicoha/tree/master/assignment4/sepia_filter/reports) - directory with time profiling reports.


#### Compilation and Usage :moyai:

`cd` into `sepia_filter` directory.

**Compile Cython Programs:**

    $ python3 setup.py build_ext --inplace

**Run individual .py programs:**

    $ python <filename>.py

This will generate time profiling reports for functions specified by the particular program.

**Generate all time profiling reports:**

    $ bash run.sh
