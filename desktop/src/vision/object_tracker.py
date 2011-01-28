'''
(c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

@author: Alex Levenson (alex@isnotinvain.com)
'''

import cPickle
import pygame
import random

from stream.video import Video
import vision.object_finder
from gui.progress_window import ProgressWindow
import util.image
from util.geometry import rect_is_similar
   
class ObjectTracker(object):
    """
    Tracks objects through a video stream
    """
    def __init__(self,video,finder=vision.object_finder.HaarFinder(),look_ahead_threshold=10,similarity=0.8):
        self.finder = finder
        self.raw_bounds = []
        self.tracks = []
        self.tracked = set()
        self.look_ahead_threshold = look_ahead_threshold
        self.similarity = similarity
        self.video = video
        self.get_tracks = False
        
                
    def _extract_raw_object_bounds(self):
        pw = ProgressWindow("Extracting Raw Bounds...")        
        for frame in self.video.frames():
            raw = self.finder.find_in_image(frame)            
            self.raw_bounds.append(raw)
            pw.set_progress(self.video.getRatio())
            pw.draw()
            if pw.get_quit(): break
    
    def _track_bound(self,bound,f):
        track = {}
        track[f] = bound
        miss_count = 0
        frame_count = 0
        while miss_count<=self.look_ahead_threshold:
            miss = True
            for b,_ in self.raw_bounds[f+frame_count]:
                if (f+frame_count,b) in self.tracked: continue
                if rect_is_similar(b,bound,self.similarity):
                    track[f+frame_count] = b
                    self.tracked.add((f+frame_count,b))
                    bound = b
                    miss_count = 0
                    miss = False
                    break
            if miss:
                miss_count += 1                          
            frame_count += 1
        return track
    
    def _extract_tracks_from_raw_object_bounds(self):        
        for f,frame_bounds in enumerate(self.raw_bounds):
            for bound,_ in frame_bounds:
                track = self._track_bound(bound,f)                
                self.tracks.append(track)
            
        
        
    
    def get_tracks(self):
        if not self.get_tracks:
            self._extract_raw_object_bounds()
            self._extract_tracks_from_raw_object_bounds()            
        return self.tracks
    
    def draw_tracks(self):
        screen = pygame.display.set_mode(map(int,self.video.get_size()))
        clock = pygame.time.Clock()
        running = True
        
        colors = []
        for track in self.tracks:
            colors.append((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        
        for f,frame in enumerate(video.frames()):            
            frame = util.image.cv_to_pygame(frame)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
            
            screen.blit(frame,(0,0))            
            
            for i,track in enumerate(self.tracks):
                if len(track) < 5: continue
                if f in track:
                    rect = pygame.Rect(*track[f])
                    pygame.draw.rect(screen,colors[i],rect,2)
                        
            pygame.display.flip()
            clock.tick(30)
            if not running: break
    
    def draw_bounds(self,video):
        screen = pygame.display.set_mode(map(int,video.get_size()))
        clock = pygame.time.Clock()
        running = True
        
        for bound in self.raw_bounds:
            #frame = video.getNextFrame()
            #frame = util.image.cv_to_pygame(frame)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
            
            #screen.blit(frame,(0,0))
            screen.fill((0,0,0))
            for b,_ in bound:
                rect = pygame.Rect(*b)
                pygame.draw.rect(screen,(0,255,0),rect,2)
            
            
            pygame.display.flip()
            clock.tick(30)
            if not running: break
    
if __name__ == "__main__":
    video = Video("/home/alex/Desktop/blarg.avi")
    t = ObjectTracker(video)
    #bounds  = t.get_raw_object_bounds(video)    
    f = open("/home/alex/Desktop/bounds.pickle","r")
    #cPickle.dump(bounds,f)
    bounds = cPickle.load(f)
    f.close()
    t.raw_bounds = bounds
    t._extract_tracks_from_raw_object_bounds()
    t.draw_tracks()
    
    #t.draw_bounds(video,bounds)