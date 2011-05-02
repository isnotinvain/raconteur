'''
Raconteur (c) Alex Levenson 2011
All rights reserved

@author: Alex Levenson (alex@isnotinvain.com)

This is for compiling and installing
'cveigenface', my custom cpython api for
calling opencv's eigenfaces functionality from
withing python

Usage: python setup.py install
'''

from distutils.core import setup, Extension

module1 = Extension('cveigenface',
                    sources=['cveigenface.c'],
                    include_dirs=["/usr/local/include/opencv"],
                    library_dirs=["/usr/local/lib"],
                    libraries=["ml", "cvaux", "highgui", "cv", "cxcore"],
                    runtime_library_dirs=["/usr/local/lib"])

setup (name='cveigenface',
       version='1.0',
       description='Runs opencv eigenface',
       ext_modules=[module1])
