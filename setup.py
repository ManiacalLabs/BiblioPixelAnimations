from __future__ import print_function
from setuptools import setup
import json
import sys
import datetime


setup(
    name='BiblioPixelAnimations',
    version=datetime.datetime.utcnow().strftime('3.%Y%m%d.%H%M%S'),
    description='BiblioPixelAnimations is an animation repository for animation classes that work with BiblioPixel: http://github.com/maniacallabs/BiblioPixel',
    author='Adam Haile',
    author_email='adam@maniacallabs.com',
    url='http://github.com/maniacallabs/BiblioPixelAnimations/',
    license='MIT',
    packages=['BiblioPixelAnimations', 'BiblioPixelAnimations.matrix',
              'BiblioPixelAnimations.strip', 'BiblioPixelAnimations.game'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
