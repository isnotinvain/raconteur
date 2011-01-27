'''
(c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

@author: Alex Levenson (alex@isnotinvain.com)
'''

from util.video import Video
import face.object_finder

class ObjectTracker(object):
    def __init__(self,video,finder=face.object_finder.HaarFinder()):
        self.video = video
        self.finder = finder
                
    def get_raw_object_bounds(self):
        bounds = {}
        for frame_no,frame in self.video.frames():
            raw = self.finder.find_in_image(frame)
            bounds[frame_no] = raw
        return bounds
    
    def get_n_raw_object_bounds(self,n=100):
        i = 0
        bounds = {}
        for frame_no,frame in self.video.frames():
            if i > n: break
            raw = self.finder.find_in_image(frame)
            bounds[frame_no] = raw
            i+=1            
        return bounds
        
    
    def classify_raw_bounds(self,raw_bounds,frame_step=5,similarity=0.90):        
        frame_nos = sorted(raw_bounds.iterkeys())
        for f in frame_nos:
            for (x,y,w,h),_ in raw_bounds[f]:
                print f, (x,y,w,h)
                
        
    def get_object_bounds(self):
        pass
    
if __name__ == "__main__":
    video = Video("/home/alex/Desktop/blarg.avi")
    t = ObjectTracker(video)
    
    b = t.get_n_raw_object_bounds()
    
    t.classify_raw_bounds(b)
    