#!/usr/bin/python
import os
import re
from setuptools import setup

# Attempt to get version number from TravisCI environment variable
version = os.environ.get('TRAVIS_TAG', default='0.0.0')

# Remove leading 'v'
version = re.sub('^v', '', version)

setup(
    name='auto-all',
    description='Automatically manage __all__ variable in Python packages.',
    version=version,
    author='Jon Grace-Cox',
    author_email='jongracecox@gmail.com',
    py_modules=['auto_all'],
    setup_requires=['setuptools', 'wheel'],
    tests_require=['unittest'],
    install_requires=[],
    data_files=[],
    options={
        'bdist_wheel': {'universal': True}
    },
    url='https://github.com/jongracecox/auto-all',
    classifiers=[
        'License :: OSI Approved :: MIT License'
    ]
)
