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
        self.bgBrush = wx.Brush((150,150,150))
        self.thumbs = {}
        self.thumbSize = None
        self.begin = None
        self.end = None
        self.totalWidth = None
        self.zoom = 1.0
        self.pos = 0.0

    def loadThumbs(self,thumbSize=(300,300)):
        self.thumbSize = thumbSize
        creations = self.parent.story.stream_creations["video"]
        files = self.parent.story.stream_files["video"]
        self.begin = creations[0]
        self.end = creations[-1]
        self.totalWidth = 0
        for creation in creations:
            video = Video(files[creation])
            frame = video.getNextFrame()
            util.image.cvScaleToSize(frame, *thumbSize)
            self.thumbs[creation] = util.image.cvToWx(frame)
            self.totalWidth += self.thumbs[creation].GetSize()[0]

    def setZoom(self,zoom):
        self.zoom = zoom
        
    def setPos(self,pos):
        self.pos = pos*self.totalWidth

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
        
        xFactor = (dcW/float(self.totalWidth)) * self.zoom
        
        x=self.pos*-1
        for creation,_ in files:
            thumb = self.thumbs[creation]
            fitSize = xFactor*thumb.GetSize()[0], dcH
            scaledWidth,scaledHeight = util.geometry.getScaledDimensions(thumb.GetSize(),fitSize)
            thumb = thumb.Scale(scaledWidth,scaledHeight,wx.IMAGE_QUALITY_NORMAL)
            thumb = wx.BitmapFromImage(thumb)
            y = dcH/2.0 - (scaledHeight/2.0)
            dc.DrawBitmap(thumb,x,y)
            dc.DrawRectangle(x,y,scaledWidth,scaledHeight)
            x+=scaledWidth