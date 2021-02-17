from distutils.core import setup

from Cython.Build import cythonize

setup(ext_modules=cythonize('cython_color2sepia.pyx',
                            compiler_directives={'language_level': "3"}),
      requires=['numpy'])
