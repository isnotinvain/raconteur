'''
Created on Feb 3, 2011

@author: Alex Levenson (alex@isnotinvain.com)
'''
import sys
import cv
import util.image
from stream.video import Video
from vision.finder import ObjectFinder

            
if __name__ == "__main__":
    if len(sys.argv) < 1: raise Exception("Requires at least one argument: <input file> <width> <height>")
    if len(sys.argv) >= 3: width,height = int(sys.argv[2]),int(sys.argv[3])
    
    video = Video(sys.argv[1]) 
    cv.NamedWindow("Face Tracking")
    
    finder = ObjectFinder("/home/alex/Documents/raconteur/desktop/src/gui/haarcascades/haarcascade_frontalface_alt.xml")
    
    for frame in video.frames():
        frame = util.image.cvScaleToSize(frame, width, height)                              
        objects = finder.findInImage(frame,scale_factor=1.1, min_neighbors=3, flags=0, min_size=(10,10))
        util.image.cvDrawObjectBoundaries(frame, objects)
        cv.ShowImage("Face Tracking",frame)
        k = cv.WaitKey(15)
        if k == '\x1b': break