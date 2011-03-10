'''
Created on Jan 6, 2011

@author: Alex Levenson (alex@isnotinvain.com)
'''
import cv
import os
import cPickle
import util.filesystem

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
        self.reset()
        
        self.face_bounds = None
        self.face_tracks = None
        self.creation = file_path[file_path.rfind("/")+1:file_path.rfind(".")]
             
    def reset(self):
        self.capture = cv.CreateFileCapture(self.file_path)
        if not self.capture or str(self.capture) == "<Capture (nil)>":
            raise Exception("Couldn't load file: " + self.file_path)  
        self.normalizedFrameNum = 0
    
    def getNextFrame(self):
        self.normalizedFrameNum += 1        
        return cv.QueryFrame(self.capture)
    
    def frames(self):
        while True:
            img = self.getNextFrame()            
            if not img: break
            yield img
    
    def getFrameNum(self):
        return cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_POS_FRAMES)

    def getNormalizedFrameNum(self):
        return self.normalizedFrameNum
    
    def getFrameCount(self):
        return cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_COUNT)
    
    def getRatio(self):
        return cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_POS_AVI_RATIO)    
        
    def getSize(self):
        return (cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_WIDTH),cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_HEIGHT))
        
    def getFps(self):
        return cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_FPS)
    
    def loadFaceBounds(self):
        p = util.filesystem.dotPrefixFilePath(self.file_path+".face_bounds.pickle")
        f = open(p,"r")
        self.face_bounds = cPickle.load(f)
        f.close()        

    def writeFaceBounds(self):
        p = util.filesystem.dotPrefixFilePath(self.file_path+".face_bounds.pickle")
        f = open(p,"w")
        cPickle.dump(self.face_bounds,f)
        f.close()
        
    def loadFaceTracks(self):
        p = util.filesystem.dotPrefixFilePath(self.file_path+".face_tracks.pickle")
        f = open(p,"r")
        self.face_tracks = cPickle.load(f)
        f.close()

    def writeFaceTracks(self):
        p = util.filesystem.dotPrefixFilePath(self.file_path+".face_tracks.pickle")
        f = open(p,"w")
        cPickle.dump(self.face_tracks,f)
        f.close()

    def printPositionData(self):
        print "Frame num: " + str(cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_POS_FRAMES))
        print "Ratio: " + str(cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_POS_AVI_RATIO))    
        print "Millis: " + str(cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_POS_MSEC))
        print "FPS: " + str(cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_FPS))
    
# proper encoding:        
# mencoder <in> -ovc lavc -lavcopts vcodec=mpeg1video:vqscale=1 -oac lavc -o <out>