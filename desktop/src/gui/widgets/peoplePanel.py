'''
Created on Feb 3, 2011

@author: Alex Levenson (alex@isnotinvain.com)
'''
import os
import wx
import stream.video
import util.image

class PeoplePanel(wx.Panel):
    '''
    A panel that draws the faces of recognized people
    in a vertical stack
    '''
    def __init__(self,parent,id,**kwargs):
        wx.Panel.__init__(self,parent,id,**kwargs)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_SIZE, self.onPaint)
        self.Bind(wx.EVT_LEFT_UP,self.onClick)
        self.bgBrush = wx.Brush((240,240,240))        
        self.bgPen = wx.TRANSPARENT_PEN
        self.videoPen = wx.Pen((100,100,100),2)
        self.videoBrush = wx.TRANSPARENT_BRUSH
        self.parent = parent
        self.faceVideos = []
        self.thumbs = []
        self.thumbSize = None
        self.zoom = 0.0
        self.pos = 0.0
        self.videoRects = None
        self.timer = wx.Timer(self, wx.ID_ANY)
        self.timer_tick = 1000/5
        self.Bind(wx.EVT_TIMER,self.onNextFrame)
        self.totalHeight = None

    def loadPeople(self):        
        self.timer.Start(self.timer_tick)
        peopleDir = os.path.join(self.parent.story.getUnrecognizedPeopleDir(),self.parent.currentVideo.creation)
        if os.path.exists(peopleDir):
            for v in os.listdir(peopleDir):
                self.faceVideos.append(stream.video.Video(os.path.join(peopleDir,v)))
        w = self.faceVideos[0].getNextFrame().width
        self.faceVideos[0].reset()
        self.thumbSize = w
        self.totalHeight = len(self.faceVideos)*self.thumbSize
    
    def pause(self):
        self.timer.Stop()
    
    def onClick(self,event):
        pass
    
    def setZoom(self,zoom):
        self.zoom = zoom
        
    def setPos(self,pos):
        self.pos = pos

    def onNextFrame(self,event):
        self.thumbs = []
        for video in self.faceVideos:
            thumb = video.getNextFrame()
            if not thumb: 
                video.reset()
                thumb = video.getNextFrame()
            self.thumbs.append((thumb,video))
        self.Refresh()
        
    def onPaint(self,event):
        dc = wx.AutoBufferedPaintDC(self)
        dcW,dcH = dc.GetSize()
        if dcW < 0 or dcH < 0: return

        dc.Clear()
        dc.SetBrush(self.bgBrush)
        dc.SetPen(self.bgPen)
        dc.DrawRectangle(0,0,dcW,dcH)
        dc = wx.AutoBufferedPaintDC(self)

        if not self.faceVideos: return
        
        dc.SetPen(self.videoPen)        
        dc.SetBrush(self.videoBrush)
        
        minScaleFactor = dcH / float(self.totalHeight)
        maxScaleFactor = dcW / float(self.thumbSize)
        deltaScale = maxScaleFactor - minScaleFactor        
        scaleFactor = minScaleFactor + self.zoom*deltaScale
         
        pplHeight = self.totalHeight*scaleFactor
        deltaOffset = pplHeight - dcH
        y = -1 * deltaOffset * self.pos
        
        self.videoRects = {}
        for thumb,video in self.thumbs:            
            img = util.image.cvToWx(thumb)
            fitsize = dcW,scaleFactor*self.thumbSize
            scaledWidth,scaledHeight = util.geometry.getScaledDimensions(img.GetSize(),fitsize)            
            img = img.Scale(scaledWidth,scaledHeight,wx.IMAGE_QUALITY_NORMAL)
            img = wx.BitmapFromImage(img)
            
            x = dcW/2.0 - (scaledWidth/2.0)
            
            dc.DrawBitmap(img,x,y)
            rect = (x,y,scaledWidth,scaledHeight)
            self.videoRects[rect] = video
            dc.DrawRectangle(*rect)
            y+=scaledHeight