from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
	include_dirs = [numpy.get_include()],
    ext_modules = cythonize("minimax.pyx")
)

#python compile.py build_ext --inplace