'''
(c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

@author: Alex Levenson (alex@isnotinvain.com)

Utilities for importing raw data from the device(s) to the file system.
Copies raw data files to the filesytem and organizes them in a useful manner
'''

import sys
import os
import shutil
import datetime
import fnmatch

import util.filesystem as fsutil

class NoSuchDirectoryError(Exception):
    pass

class NoSuchFileError(Exception):
    pass

class StreamImporter(object):
    """
    A default generic stream importer, can be used directly to import streams that
    require no pre-processing aside from file copying, renaming, and placement into
    a structured folder hierarchy. Can be subclassed in order to handle pre-processing
    of streams.
    """
    
    def __init__(self,stream_type,root_destination_dir,move=False):
        """
        @param stream_type: a string representing what kind of stream this is, eg "video" or "image" or "gps"
                            should be a valid folder name in the filesystem
        
        @param root_destination_dir: path to the top level directory where this stream should be imported to
        @raise OSError:
        
        @raise NotADirectoryError:        
        """

        self.stream_type= stream_type
        self.root_destination_dir = root_destination_dir
        self.move = move
        
        #check if dir_path exists / create it if it doesn't
        try:
            fsutil.ensure_dir_exists(self.root_destination_dir)
        except OSError:
            print self.root_destination_dir + " does not exist and could not be created."
            raise
        except fsutil.NotADirectoryError:
            print self.root_destination_dir + " is not a directory!"
            raise
        
    def import_dir(self,dir_path,filter_function=None):
        """
        imports the contents of a directory to self.root_destination_dir
                        
        @param filter_function: will be called on each file encountered to
        determine whether or not to import it
        
        @raise NoSuchDirectoryError: if dir_path does not exist
        """
        if not os.path.exists(dir_path):
            raise NoSuchDirectoryError(dir_path)
                
        # process each file in dir_path (recursively)
        for root,_,files in os.walk(dir_path):
            for name in files:
                path = os.path.join(root,name)
                if filter_function:
                    if filter_function(path):                        
                        self.import_file(path)
                else:
                    self.import_file(path)
        print "Done!"
                    
    def import_file(self,file_path):
        """
        imports file_path to self.root_destination_dir
        
        if move is set to true, files are moved not copied
        
        Files are organized hierarchically in following manner, based on the file's
        date of creation metadata:
        
        year (int)
            month (int)
                day (int)
                    stream_type (string)
                        X.<original file extension>
        
        Where X is an integer
        TODO: X should have some meaning, perhaps sort order by date of creation?
        """
        
        # make sure the file exists
        if not os.path.exists(file_path):
            raise NoSuchFileError(file_path)
                
        if self.move:
            copy_function = shutil.move
            copy_verb = "moving"
        else:
            copy_function = shutil.copy2
            copy_verb = "copying"    
            
        
        # get the file's creation date
        # TODO: actually check creation date, not modified date
        start_stamp = os.path.getmtime(file_path)
        start_date = datetime.datetime.fromtimestamp(start_stamp)
        
        # figure out where to put the file
        dest_dir = fsutil.stream_raw_data_path(start_date, self.stream_type)
        dest_dir = os.path.join(self.root_destination_dir,dest_dir)
        _, extension = os.path.splitext(file_path)
        filename = fsutil.unique_file_name(self.root_destination_dir,extension,str(int(start_stamp)))                
        dest_file = os.path.join(dest_dir,filename)
        
        # make sure dest_dir exists
        fsutil.ensure_dir_exists(dest_dir)
        
        #copy the file
        print copy_verb + " " + file_path + " to " + dest_file
        copy_function(file_path,dest_file)

if __name__ == "__main__":
    if len(sys.argv) < 4: raise Exception("Requires 3 or 5 command line arguments: <source file or directory> <destination directory> <stream type> |optional| <unix wildcards> <move>")    
    
    if len(sys.argv) >= 5:
        filter = lambda x : fnmatch.fnmatch(x,sys.argv[4])
    else:
        filter = None    
    
    move = False
    if len(sys.argv) >= 6:
        if sys.argv[5] == "move":
            move = True
                                
    if not os.path.exists(sys.argv[1]):
        raise Exception(sys.argv[1]+" is not a valid path")

    importer = StreamImporter(sys.argv[3],sys.argv[2],move)
    
    if os.path.isdir(sys.argv[1]):   
        importer.import_dir(sys.argv[1],filter)
    else:
        importer.import_file(sys.argv[1],filter)
        