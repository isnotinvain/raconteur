'''
Created on Feb 8, 2011

@author: Alex Levenson (alex@isnotinvain.com)

Video overlays for HUD layers on top of video
'''
import wx
import random

def overlayFromFaceBounds(face_bounds):
        rectSprites = {}
        for frameNo,listOfBounds in enumerate(face_bounds):            
            rectSprites[frameNo] = []
            for (x,y,w,h),_ in listOfBounds:
                rectSprites[frameNo].append(Rect(x,y,w,h))                
        return VideoOverlay(rectSprites)               

def overlayFromTracks(tracks,face_bounds):
    colors = {}
    for track in tracks:
        colors[id(track)] = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    rectSprites = {}
    for frameNo in xrange(len(face_bounds)):
        rectSprites[frameNo] = []
        for track in tracks:                
            if frameNo in track:
                rectSprites[frameNo].append(Rect(*track[frameNo],color=colors[id(track)]))
                
    return VideoOverlay(rectSprites)

class VideoOverlaySprite(object):
    """
    Base class for sprites in video overlays
    """
    def draw(self,dc,scaleFactor):
        """
        Draw this object to dc
        """
        pass
        
class VideoOverlay(object):
    """
    Base class for video over lays
    """
    def __init__(self,sprites = {}):
        self.sprites = sprites
        self.scale = 1.0
    
    def drawFrame(self,dc,scaleFactor,frameNo):
        """
        Draw this video overlay for a specific frame
        """

        if frameNo in self.sprites:
            for sprite in self.sprites[frameNo]:
                sprite.draw(dc,scaleFactor)


class Rect(VideoOverlaySprite):
    """
    A simple rectangle with color
    """
    
    def __init__(self,x,y,w,h,color=(0,255,0),fillColor=None,penWidth=1):                
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
        self.color = color
        self.fillColor = fillColor
        self.penWidth = penWidth
        
        # scaled information
        self.sx = x
        self.sy = y
        self.sw = w
        self.sh = h
        self.oldScaleFactor = 1.0
        self.scaleFactor = 1.0
        
        self.pen = wx.Pen(self.color, self.penWidth)        
        if self.fillColor:
            self.brush = wx.Brush(self.fillColor)
        else:
            self.brush = wx.Brush((0,0,0),style=wx.TRANSPARENT) 

    def scale(self,factor):
        self.sx = self.x * factor
        self.sy = self.y * factor
        self.sw = self.w * factor
        self.sh = self.h * factor        
        
    def draw(self,dc,scaleFactor):
        if not self.oldScaleFactor or self.oldScaleFactor != scaleFactor:
            self.scale(scaleFactor)
        
        dc.SetPen(self.pen)
        dc.SetBrush(self.brush)
        dc.DrawRectangle(self.sx,self.sy,self.sw,self.sh)