'''
(c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

@author: Alex Levenson (alex@isnotinvain.com)
'''
import cv

import face.object_finder

class ObjectTracker(object):
    def __init__(self,video,finder=face.object_finder.HaarFinder()):
        self.video = video
        self.finder = finder
        
    def get_raw_object_bounds(self):
        bounds = {}
        for frame in self.video.frames():
            frame_no,raw = self.finder.find_in_image(frame)
            bounds[frame_no] = raw
        return bounds
    
    def draw_raw_bounds(self,img,bounds,frame_no,color=(255,0,0)):
        for (x,y,w,h),_ in bounds[frame_no]:
            cv.Rectangle(img, (x,y), (x+w,y+h), color)
        