'''
Created on Jan 6, 2011

@author: Alex Levenson (alex@isnotinvain.com)
'''
import sys
import cv
import os

# TODO: inherit from some Stream object probably
class Video(object):
    """
    A more pythonic wrapper for video streams, currently wraps openCV videos
    TODO: create a stream interface and conform to it
    """
    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.exists(file_path):
            raise Exception("Couldn't load file: " + file_path) 
        self.capture = cv.CreateFileCapture(file_path)    
        if not self.capture:
            raise Exception("Couldn't load file: " + file_path)
        
    
    def getNextFrame(self):
        return cv.QueryFrame(self.capture)
    
    def frames(self):
        while True:
            img = self.getNextFrame()            
            if not img: break
            yield img
    
    def getRatio(self):
        return cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_POS_AVI_RATIO)    
    
    def print_position(self):
        print "Frame num: " + str(cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_POS_FRAMES))
        print "Ratio: " + str(cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_POS_AVI_RATIO))    
        print "Millis: " + str(cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_POS_MSEC))
        print "FPS: " + str(cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_FPS))
    
    def get_size(self):
        return (cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_WIDTH),cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_HEIGHT))
            
if __name__ == "__main__":
    if len(sys.argv) < 2: raise Exception("Must specify a video file")
    video = Video(sys.argv[1])    
    for _,frame in video.frames():
        video.print_position()
        cv.ShowImage("Video Test", frame)
        k = cv.WaitKey(10)
        if k != -1: break
    
    while True:
        k = cv.WaitKey(10)
        if k != -1: break

# proper encoding:        
# mencoder <in> -ovc lavc -lavcopts vcodec=mpeg1video:vqscale=1 -oac lavc -o <out>