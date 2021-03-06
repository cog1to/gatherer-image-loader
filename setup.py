"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['ImageLoaderController.py']
DATA_FILES = ['ImageLoaderWindow.xib']
OPTIONS = {'includes': ['lxml.etree', 'lxml._elementpath', 'gzip', 'threading']}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
