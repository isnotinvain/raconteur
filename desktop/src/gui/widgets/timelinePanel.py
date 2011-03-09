'''
Created on Feb 3, 2011

@author: Alex Levenson (alex@isnotinvain.com)
'''
import wx
import util.image
from stream.video import Video


class TimelinePanel(wx.Panel):
    '''
    A panel that draws the faces of recognized people
    in a vertical stack
    '''
    def __init__(self,parent,id,**kwargs):
        wx.Panel.__init__(self,parent,id,**kwargs)
        self.parent = parent
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_SIZE, self.onPaint)
        self.Bind(wx.EVT_LEFT_UP,self.onClick)
        self.bgBrush = wx.Brush((0,0,0))
        self.thumbs = {}
        self.thumbSize = None
        self.begin = None
        self.end = None
        self.totalWidth = None
        self.totalHeight = None
        self.zoom = 0.0
        self.pos = 0.0
        self.videoRects = None

    def loadThumbs(self,thumbSize=(300,300)):
        self.thumbSize = thumbSize
        creations = self.parent.story.stream_creations["video"]
        files = self.parent.story.stream_files["video"]
        self.begin = creations[0]
        self.end = creations[-1]
        self.totalWidth = 0
        self.totalHeight = 0
        for creation in creations:
            video = Video(files[creation])
            frame = video.getNextFrame()
            util.image.cvScaleToSize(frame, *thumbSize)
            self.thumbs[creation] = util.image.cvToWx(frame)
            w,h = self.thumbs[creation].GetSize()
            self.totalWidth += w            
            if h > self.totalHeight: self.totalHeight = h 

    def setZoom(self,zoom):
        self.zoom = zoom
        
    def setPos(self,pos):
        self.pos = pos

    def onClick(self,event):
        if not self.videoRects: return
        pt = event.m_x,event.m_y
        rect = util.geometry.pointInWhichRect(pt, self.videoRects.iterkeys())
        if rect == None: return
        print self.videoRects[rect]
        
    def onPaint(self,event):
        dc = wx.PaintDC(self)
        dcW,dcH = dc.GetSize()
        if dcW < 0 or dcH < 0: return

        dc.Clear()
        dc.SetBrush(self.bgBrush)
        dc.SetPen(wx.TRANSPARENT_PEN)        
        dc.DrawRectangle(0,0,dcW,dcH)
        
        if not self.parent.story: return
                
        dc.SetPen(wx.Pen((0,0,175),2))        
        dc.SetBrush(wx.TRANSPARENT_BRUSH)        
        
        files = self.parent.story.getStreamsInRange(self.begin,self.end,"video")
        
        minScaleFactor = dcW/float(self.totalWidth)
        maxScaleFactor = dcH/float(self.totalHeight)        
        deltaScale = maxScaleFactor - minScaleFactor        
        scaleFactor = minScaleFactor + self.zoom*deltaScale 
        
        timelineWidth = self.totalWidth*scaleFactor
        deltaOffset = timelineWidth - dcW
        x = -1 * deltaOffset * self.pos
        
        self.videoRects = {}
        for creation,file in files:
            thumb = self.thumbs[creation]
            fitSize = scaleFactor*thumb.GetSize()[0], dcH
            scaledWidth,scaledHeight = util.geometry.getScaledDimensions(thumb.GetSize(),fitSize)
            thumb = thumb.Scale(scaledWidth,scaledHeight,wx.IMAGE_QUALITY_NORMAL)
            thumb = wx.BitmapFromImage(thumb)
            y = dcH/2.0 - (scaledHeight/2.0)
            dc.DrawBitmap(thumb,x,y)
            rect = (x,y,scaledWidth,scaledHeight)
            self.videoRects[rect] = (creation,file)
            dc.DrawRectangle(*rect)
            x+=scaledWidth