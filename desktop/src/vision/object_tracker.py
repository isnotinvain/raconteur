'''
(c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

@author: Alex Levenson (alex@isnotinvain.com)
'''

import pygame
from stream.video import Video
import vision.object_finder
import cPickle
from gui.progress_window import ProgressWindow
import Image
import cv

class ObjectTracker(object):
    """
    Tracks objects through a video stream
    """
    def __init__(self,finder=vision.object_finder.HaarFinder()):
        self.finder = finder
                
    def get_raw_object_bounds(self,video):
        pw = ProgressWindow("Getting Raw Bounds...")
        bounds = []
        for frame in video.frames():
            raw = self.finder.find_in_image(frame)            
            bounds.append(raw)
            pw.set_progress(video.getRatio())
            pw.draw()
            if pw.get_quit(): break
        return bounds
    
    def draw_bounds(self,video,bounds):
        screen = pygame.display.set_mode(map(int,video.get_size()))
        clock = pygame.time.Clock()
        running = True
        
        for bound in bounds:
            frame = video.getNextFrame()
            cv.CvtColor(frame, frame, cv.CV_BGR2RGB)
            pil = Image.fromstring("RGB", cv.GetSize(frame), frame.tostring())            
            py_img = pygame.image.frombuffer(pil.tostring(), pil.size, pil.mode)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
            
            screen.blit(py_img,(0,0))
            
            for b,_ in bound:
                rect = pygame.Rect(*b)
                pygame.draw.rect(screen,(0,255,0),rect,2)
            
            
            pygame.display.flip()
            clock.tick(30)
            if not running: break

'''        
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
 '''
    
if __name__ == "__main__":
    video = Video("/home/alex/Desktop/blarg.avi")
    t = ObjectTracker()      
    #bounds  = t.get_raw_object_bounds(video)    
    f = open("/home/alex/Desktop/bounds.pickle","r")
    #cPickle.dump(bounds,f)
    bounds = cPickle.load(f)
    f.close()
    
    t.draw_bounds(video,bounds)
    
    