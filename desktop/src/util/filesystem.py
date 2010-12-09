'''
(c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

@author: Alex Levenson (alex@isnotinvain.com)
'''

import os

class NotADirectoryError(Exception):
    pass

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