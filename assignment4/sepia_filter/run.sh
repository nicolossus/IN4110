# Run script to generate timing reports
python3 python_color2sepia.py
python3 numpy_color2sepia.py
python3 numba_color2sepia.py
python3 setup.py build_ext --inplace
python3 benchmark_cython_color2sepia.py
