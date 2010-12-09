'''
(c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

@author: Alex Levenson (alex@isnotinvain.com)

Utilities for importing raw data from the device(s) to the file system.
Copies raw data files to the filesytem and organizes them in a useful manner
'''

import sys
import os
from util.filesystem import ensure_dir_exists, NotADirectoryError

class NoSuchDirectoryError(Exception):
    pass

class StreamImporter(object):
    """
    A default generic stream importer, can be used directly to import streams that
    require no pre-processing aside from file copying, renaming, and placement into
    a structred folder hierarchy. Can be subclassed in order to handle pre-processing
    of streams.
    """
    
    def __init__(self,stream_type,destination_dir_path):
        """
        @param stream_type: a string representing what kind of stream this is, eg "video" or "image" or "gps"
                            should be a valid folder name in the filesystem
        
        @param destination_dir_path: path to the top level directory where this stream should be imported to
        """
        self.stream_type= stream_type
        self.destination_dir_path = destination_dir_path
        
    def import_dir(self,dir_path,filter_function=lambda x: True):
        """
        imports the contents of a directory to self.destination_dir_path
                        
        @param filter_function: will be called on each file encountered to
        determine whether or not to import it
        
        @raise OSError:
        
        @raise NotADirectoryError:
        
        @riase NoSuchDirectoryError: if dir_path does not exist
        """
        
        #check if dir_path exists / create it if it doesn't
        try:
            ensure_dir_exists(self.destination_dir_path)
        except OSError:
            print self.destination_dir_path + " does not exist and could not be created."
            raise
        except NotADirectoryError:
            print self.destination_dir_path + " is not a directory!"
            raise
        
        if not os.path.exists(dir_path):
            raise NoSuchDirectoryError(dir_path)
        
        # process each file in dir_path (recursively)
        for root,_,files in os.walk(dir_path):
            for name in files:
                path = os.path.join(root,name)
                if filter_function(path):
                    self.import_file(path)
        
    def import_file(self,file_path):
        """
        imports file_path to self.destination_dir_path
        
        Files are organized hierarchically in following manner, based on the file's
        date of creation metadata:
        
        year
            month
                day
                    stream_type
                        X.<original file extension>
        
        Where X is an integer, starting at 1 and counting up, in order of time of creation. Ties will be broken arbitrarily
        """
        print file_path
        
if __name__ == "__main__":
    if not len(sys.argv) == 4: raise Exception("Requires 3 command line arguments: <source file or directory> <destination directory> <stream type>")
    
    importer = StreamImporter(sys.argv[3],sys.argv[2])
    
    if os.path.isdir(sys.argv[1]):        
        importer.import_dir(sys.argv[1])
    else:
        importer.import_file(sys.argv[1])
        