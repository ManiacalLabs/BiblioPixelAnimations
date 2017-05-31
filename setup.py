from __future__ import print_function
from setuptools import setup, find_packages
import json
import sys
import datetime


def _get_version():
    from os.path import abspath, dirname, join
    filename = join(dirname(abspath(__file__)), 'VERSION')
    print('Reading version from {}'.format(filename))
    version = open(filename).read().strip()
    print('Version: {}'.format(version))
    return version


setup(
    name='BiblioPixelAnimations',
    version=_get_version(),
    description='BiblioPixelAnimations is an animation repository for animation classes that work with BiblioPixel: http://github.com/maniacallabs/BiblioPixel',
    author='Adam Haile',
    author_email='adam@maniacallabs.com',
    url='http://github.com/maniacallabs/BiblioPixelAnimations/',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
