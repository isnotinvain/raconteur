'''
Created on Jan 6, 2011

@author: Alex Levenson (alex@isnotinvain.com)
'''
import cv
import os
import cPickle
import util.filesystem
import gst

# TODO: inherit from some Stream object probably
class CvVideo(object):
    """
    A more pythonic wrapper for video streams, currently wraps openCV videos
    TODO: create a stream interface and conform to it
    """
    
    @classmethod
    def getCreation(cls,file_path):
        return file_path[file_path.rfind("/")+1:file_path.rfind(".")]
    
    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.exists(file_path):
            raise Exception("Couldn't load file: " + file_path) 
        self.reset()
        
        self.face_bounds = None
        self.face_tracks = None
        self.creation = self.getCreation(file_path)
        self.duration = None
        self.normalizedFrameCount = 0
             
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
    
    def calcDuration(self):
        d = gst.parse_launch("filesrc name=source ! decodebin2 ! fakesink")
        source = d.get_by_name("source")
        source.set_property("location", self.file_path)
        d.set_state(gst.STATE_PLAYING)
        d.get_state()
        format = gst.Format(gst.FORMAT_TIME)
        duration = d.query_duration(format)[0]
        d.set_state(gst.STATE_NULL)
        self.duration = duration / gst.SECOND
        self.normalizedFrameCount = int(self.getFps() * self.duration) 
    
    def getNormalizedFrameCount(self):
        return self.normalizedFrameCount
    
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