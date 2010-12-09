'''
(c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

@author: Alex Levenson (alex@isnotinvain.com)
'''

import os
import random

class NotADirectoryError(Exception):
    pass

def unique_file_name(dir,extension):
    """
    generate a filename that does not exist in dir
    TODO: let's use something more descriptive about the file?
    """
    extension = extension.lower()
    f = str(random.randint(0,100000000000)) + extension
    while os.path.exists(os.path.join(dir,f)):
        f = str(random.randint(0,100000000000)) + extension

    return f

def datetime_to_path(d):
    """
    convert a datetime to a file path in the form:
    year/month/day/
    """
    return os.path.join(str(d.year),str(d.month),str(d.day))

def stream_raw_data_path(start_date,stream_type):
    """
    return the folder that a raw datafile would be found in
    given datetime start_date
    
    @param start_date: a datetime representing the beginning of the raw datafile
    @param stream_type: a string describing the type of stream, eg "video"
    """
    
    return os.path.join(datetime_to_path(start_date),stream_type)

def ensure_dir_exists(dir_path):
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