from __future__ import print_function
from setuptools import setup, find_packages
from sys import version_info as vi


if vi.major != 3:
    ver = '{}.{}.{}'.format(vi.major, vi.minor, vi.micro)
    error = (
        'INSTALLATION WARNING!\n'
        'BiblioPixelAnimations requires Python 3.4+ and you are using {}!\n'
        'All versions after v3.20170531.153148 are designed for BiblioPixel 3.x and Python 3.4+\n'
        'If you absolutely require using Python 2, '
        'please install the older version using:\n'
        '> pip install BiblioPixelAnimations==3.20170531.153148 --upgrade'
        '\n'
        'However, we highly recommend using the latest BiblioPixel '
        '(v3+) and BiblioPixelAnimations with Python 3.4+\n'
        '\n'
    )
    print(error.format(ver))


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
    packages=find_packages() + ['Graphics', 'Projects'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
