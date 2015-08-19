from distutils.core import setup
import BiblioPixelAnimations
import urllib2, json
head = urllib2.urlopen("https://api.github.com/repos/ManiacalLabs/BiblioPixelAnimations/git/refs/head").read()
head_data = json.loads(head)
_ver = "9.9.9b"
if len(head_data) > 0:
    _ver = head_data[0]["object"]["sha"]

print __file__

setup(
    name='BiblioPixelAnimations',
    version=_ver,
    description='BiblioPixelAnimations is an animation repository for animation classes that work with BiblioPixel: http://github.com/maniacallabs/BiblioPixel',
    author='Adam Haile',
    author_email='adam@maniacallabs.com',
    url='http://github.com/maniacallabs/BiblioPixelAnimations/',
    license='MIT',
    packages=['BiblioPixelAnimations', 'BiblioPixelAnimations.matrix', 'BiblioPixelAnimations.strip'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
