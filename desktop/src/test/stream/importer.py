'''
Created on Feb 3, 2011

@author: Alex Levenson (alex@isnotinvain.com)
'''
import sys
import os
import fnmatch
from stream.importer import StreamImporter

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
        importer.importDirectory(sys.argv[1],filter)
    else:
        importer.importFile(sys.argv[1],filter)
        