import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="PySciPlotTK",
    version="0.1.0",
    author="Rafael Reiter",
    author_email="mail@zonk.at",
    description="Python Scientific Plot Toolkit",
    license="BSD",
    keywords="solid state physics tight binding",
    url="https://github.com/zonksoft/envTB",
    packages=find_packages(exclude=['tools']),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
    ],
)
