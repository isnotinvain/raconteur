'''
Created on Jan 7, 2011

@author: Alex Levenson (alex@isnotinvain.com)
'''
import sys
import cv

from stream.video import Video

class VideoConverter:
    """
    A really naiive video encoder that loads each frame from a video and then writes it 
    to another video file. This (hopefully) makes an opencv friendly video.
    
    TODO: Never use this, get rid of it, it's terrible and stupid. And doesn't really work.
    """
    def __init__(self,video,out_path,fourcc = ('P','I','M','1')):
        self.out_path = out_path
        self.fourcc = fourcc
        self.video = video
        self.writer = cv.CreateVideoWriter(self.out_path, \
            cv.CV_FOURCC(*self.fourcc), \
            cv.GetCaptureProperty(self.video.capture,cv.CV_CAP_PROP_FPS), \
            video.get_size(), \
            True)
    
    def convert(self):
        for _,frame in self.video.frames():
            cv.WriteFrame(self.writer,frame)

if __name__ == "__main__":
    if len(sys.argv) < 3: raise Exception("Must specify in file and out file")
    video = Video(sys.argv[1])
    converter = VideoConverter(video,sys.argv[2])
    converter.convert()
    print "done!"