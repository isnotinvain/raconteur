'''
(c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

@author: Alex Levenson (alex@isnotinvain.com)

Utilities for importing raw data from the device(s) to the file system.
Copies raw data files to the filesytem and organizes them in a useful manner
'''

class StreamImporter(object):
    """
    A default generic stream importer, can be used directly to import streams that
    require no pre-processing aside from file copying, renaming, and placement into
    a structred folder hierarchy. Can be subclassed in order to handle pre-processing
    of streams.
    """
    
    def __init__(self,stream_type,destination_directory_path):
        """
        @param stream_type: a string representing what kind of stream this is, eg "video" or "image" or "gps"
                            should be a valid folder name in the filesystem
        
        @param destination_directory_path: path to the top level directory where this stream should be imported to
        """
        self.stream_type= stream_type
        self.destination_directory_path = destination_directory_path
        
    def import_directory(self,directory_path,filter_function=None,recursive=False):
        """
        imports the contents of a directory to self.destination_directory_path
        
        Files are organized hierarchically in following manner, based on the file's
        date of creation metadata:
        
        year
            month
                day
                    stream_type
                        X.<original file extension>
        
        Where X is an integer, starting at 1 and counting up, in order of time of creation. Ties will be broken arbitrarily
                
        @param filter_function: if is set, it will be called on each file encountered to
        determine whether or not to import it
        
        @param recursive: whether or not to recurse into sub directories
        """
        pass
    
    