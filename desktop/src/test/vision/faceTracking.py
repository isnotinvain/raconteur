'''
Created on Feb 3, 2011

@author: Alex Levenson (alex@isnotinvain.com)
'''
import sys
import cPickle
import random
import pygame
import stream.video
import vision.tracker
import gui.progress_window
import gui.progressTracker
import util.image

def pwCallback(pw,pt,p):
    pw.set_progress(p)
    pw.draw()
    if pw.get_quit():
        pt.requestAbort()

if __name__ == "__main__":
    if len(sys.argv) < 1: raise Exception("Must specify an input file")
    if len(sys.argv) > 2: 
        pickle = sys.argv[2]
    else:
        pickle = None
    notrack = False
    if len(sys.argv) > 3:
        if sys.argv[3] == "notrack": notrack = True
    
    video = stream.video.Video(sys.argv[1])
    finder = vision.finder.ObjectFinder("/home/alex/Documents/raconteur/desktop/src/gui/haarcascades/haarcascade_frontalface_alt.xml")
    tracker = vision.tracker.ObjectTracker(video,objFinder=finder)
        
    if not pickle:
        pw = gui.progress_window.ProgressWindow("Extracting")    
        progressTracker = gui.progressTracker.ProgressTracker(lambda p: pwCallback(pw,progressTracker,p))
        tracker.progressTracker = progressTracker
        tracks = tracker.getObjectTracks()
    else:
        f = open(pickle,"r")
        bounds = cPickle.load(f)
        f.close()
        tracks = tracker.getObjectTracks(bounds)
    
    video.reset()
    
    screen = pygame.display.set_mode(map(int,video.getSize()))
    clock = pygame.time.Clock()
    running = True
    
    colors = []
    for track in tracks:
        colors.append((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    
    for f,frame in enumerate(video.frames()):
        frame = util.image.cvToPygame(frame)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
        
        screen.blit(frame,(0,0))
        
        if not notrack:
            for i,track in enumerate(tracks):
                if len(track) < 20: continue
                if f in track:
                    rect = pygame.Rect(*track[f])
                    pygame.draw.rect(screen,colors[i],rect,2)
        else:
            for bound in bounds[f]:
                rect = pygame.Rect(bound[0][0],bound[0][1],bound[0][2],bound[0][3])
                pygame.draw.rect(screen,(0,255,0),rect,2)
            
        pygame.display.flip()
        clock.tick(30)
        if not running: break