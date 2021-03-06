'''
Raconteur (c) Alex Levenson 2011
All rights reserved

@author: Alex Levenson (alex@isnotinvain.com)

Filesystem utility functions
'''

import os
import cPickle
import random

class NotADirectoryError(Exception):
    pass

def dotPrefixFilePath(path):
    """
    takes a path like
        a/b/c.txt
    and makes it:
        a/b/.c.txt
    """
    lastSlash = path.rfind("/")
    d = path[:lastSlash + 1]
    f = path[lastSlash + 1:]
    f = "." + f
    return os.path.join(d, f)

def generateUniqueFileName(dir, extension, prefix=""):
    """
    generate a filename that does not exist in dir that begins with prefix
    if <prefix>.<extension> does not exist, then it is used.
    """
    extension = extension.lower()

    if prefix and not os.path.exists(os.path.join(dir, prefix + extension)):
        return prefix + extension

    f = prefix + "_" + str(random.randint(0, 100000000000)) + extension
    while os.path.exists(os.path.join(dir, f)):
        f = prefix + "_" + str(random.randint(0, 100000000000)) + extension

    return f

def datetimeToPath(d):
    """
    convert a datetime to a file path in the form:
    year/month/day/
    """
    return os.path.join(str(d.year), str(d.month), str(d.day))

def getStreamRawDataPath(start_date, stream_type):
    """
    return the folder that a raw datafile would be found in
    given datetime start_date

    @param start_date: a datetime representing the beginning of the raw datafile
    @param stream_type: a string describing the type of stream, eg "video"
    """

    return os.path.join(datetimeToPath(start_date), stream_type)

def ensureDirectoryExists(dir_path):
    """
    Checks that:
        1) dir_path exists
        2) dir_path is a directory

    If dir_path does not exist, tries to create it

    @param dir_path: path to the directory being checked / created

    @raise OSError: if dir_path does not exist and cannot be created

    @raise NotADirectoryError: if dir_path exists but is not a directory
    """

    if not os.path.exists(dir_path):
        # this may raise an OSError
        os.makedirs(dir_path)

    if not os.path.isdir(dir_path):
        raise NotADirectoryError(dir_path)
