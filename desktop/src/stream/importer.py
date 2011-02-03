'''
(c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

@author: Alex Levenson (alex@isnotinvain.com)

Utilities for importing raw data from the device(s) to the file system.
Copies raw data files to the filesytem and organizes them in a useful manner
'''
import os
import shutil
import datetime

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
            fsutil.ensureDirectoryExists(self.root_destination_dir)
        except OSError:
            print self.root_destination_dir + " does not exist and could not be created."
            raise
        except fsutil.NotADirectoryError:
            print self.root_destination_dir + " is not a directory!"
            raise
        
    def importDirectory(self,dir_path,filter_function=None):
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
                        self.importFile(path)
                else:
                    self.importFile(path)
        print "Done!"
                    
    def importFile(self,file_path):
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
        dest_dir = fsutil.getStreamRawDataPath(start_date, self.stream_type)
        dest_dir = os.path.join(self.root_destination_dir,dest_dir)
        _, extension = os.path.splitext(file_path)
        filename = fsutil.generateUniqueFileName(self.root_destination_dir,extension,str(int(start_stamp)))                
        dest_file = os.path.join(dest_dir,filename)
        
        # make sure dest_dir exists
        fsutil.ensureDirectoryExists(dest_dir)
        
        #copy the file
        print copy_verb + " " + file_path + " to " + dest_file
        copy_function(file_path,dest_file)