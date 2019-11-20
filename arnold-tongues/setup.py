from distutils . core import setup
from Cython . Build import cythonize
#from distutils . extension import Extension
import numpy

#extensions = [ Extension ('source', [ 'tonglib.pyx'] ) ]
# extra_compile_flags = "-stdlib=libc++"
setup(
 ext_modules = cythonize ("tonglib.pyx", gdb_debug = True),
 include_dirs = [ numpy . get_include () ]
)
