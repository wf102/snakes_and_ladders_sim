from setuptools import setup, Extension
from Cython.Build import cythonize

ext = Extension(
    name="multigame",
    sources=["multigame.pyx", "multigame_core.cpp"],
    language="c++",
)

setup(
    ext_modules=cythonize(ext),
)