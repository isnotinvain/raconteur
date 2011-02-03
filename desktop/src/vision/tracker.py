'''
(c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

@author: Alex Levenson (alex@isnotinvain.com)
'''

import finder
import util.geometry
import gui
   
class ObjectTracker(object):
    """
    Tracks objects through a video stream
    """
    def __init__(self,video,finder=finder.ObjectFinder(),look_ahead_threshold=30,similarity=0.5):
        self.finder = finder
        self.raw_bounds = None
        self.tracks = None
        self.tracked = set()
        self.look_ahead_threshold = look_ahead_threshold
        self.similarity = similarity
        self.video = video        
        self.progressTracker = None
                                
    def __extractRawObjectBounds(self):
        """
        Runs object detection on each frame of the video,
        this can be quite slow.
        """
        self.raw_bounds = []
        if self.progressTracker: self.progressTracker.currentProcess = "Extracting raw object bounds"
        for frame in self.video.frames():
            raw = self.finder.findInImage(frame)            
            self.raw_bounds.append(raw)
            if self.progressTracker:                
                self.progressTracker.tick(self.video.getRatio())            
                if self.progressTracker.abort: break
                            
    def __trackBound(self,bound,f):
        """
        Track a single bound through the video
        """
        track = {}
        track[f] = bound
        miss_count = 0
        frame_count = 0
        while miss_count<=self.look_ahead_threshold:
            miss = True
            if f+frame_count >= len(self.raw_bounds): break
            for b,_ in self.raw_bounds[f+frame_count]:
                if (f+frame_count,b) in self.tracked: continue
                if util.geometry.rectIsSimilar(b,bound,self.similarity):
                    track[f+frame_count] = b
                    #self.tracked.add((f+frame_count,b))
                    bound = b
                    miss_count = 0
                    miss = False
                    break
            if miss:
                miss_count += 1                          
            frame_count += 1
        return track
    
    def __extractTracksFromRawObjectBounds(self):
        """
        The main algorithm of the ObjectTracker,
        Crawls through the raw object bounds and tries
        to guess which bounds correspond to the same object
        across frames, using locality
        """        
        self.tracks = []
        for f,frame_bounds in enumerate(self.raw_bounds):
            for bound,_ in frame_bounds:                
                track = self.__trackBound(bound,f)
                if len(track) > 5:
                    self.tracks.append(track)
                    for t in track.iteritems():
                        self.tracked.add(t)
   
    def getObjectTracks(self,raw=None):
        if not self.tracks:
            if raw: self.raw_bounds = raw
            if not self.raw_bounds:
                self.__extractRawObjectBounds()
            self.__extractTracksFromRawObjectBounds()            
        return self.tracks