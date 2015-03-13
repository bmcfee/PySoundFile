#!/usr/bin/env python
import sys
from setuptools import setup, Distribution
from setuptools.command.test import test as TestCommand
from sys import platform
from platform import architecture

if platform == 'win32' and architecture()[0] == '32bit':
    libsndfile = ['win32/libsndfile.dylib', 'libsndfile_license']
elif platform == 'win32' and architecture()[0] == '64bit':
    libsndfile = ['win64/libsndfile.dylib', 'libsndfile_license']
elif platform == 'darwin':
    libsndfile = ['darwin/libsndfile.dylib', 'libsndfile_license']
else:
    libsndfile = []


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


class BinaryDistribution(Distribution):
    def is_pure(self):
        return False


setup(
    name='PySoundFile',
    version='0.6.0',
    description='An audio library based on libsndfile, CFFI and NumPy',
    author='Bastian Bechtold',
    author_email='basti@bastibe.de',
    url='https://github.com/bastibe/PySoundFile',
    keywords=['audio', 'libsndfile'],
    packages=['pysoundfile_binaries'],
    package_data={'pysoundfile_binaries':libsndfile},
    py_modules=['soundfile'],
    license='BSD 3-Clause License',
    install_requires=['numpy',
                      'cffi>=0.6'],
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Multimedia :: Sound/Audio'
    ],
    long_description=open('README.rst').read(),
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    distclass=BinaryDistribution,
)
