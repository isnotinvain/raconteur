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

    def loadThumbs(self,thumbSize=(300,300)):
        self.thumbSize = thumbSize
        creations = self.parent.story.file_creations["video"]
        files = self.parent.story.raw_files["video"]
        self.begin = creations[0]
        self.end = creations[-1]
        
        self.begin = 1293858686
        self.end = 1293862542
        
        for creation in creations:
            video = Video(files[creation])
            frame = video.getNextFrame()
            util.image.cvScaleToSize(frame, *thumbSize)
            self.thumbs[creation] = util.image.cvToWx(frame)


    def onPaint(self,event):
        dc = wx.PaintDC(self)
        dcW,dcH = dc.GetSize()
        if dcW < 0 or dcH < 0: return

        dc.Clear()
        dc.SetBrush(self.bgBrush)
        dc.SetPen(wx.TRANSPARENT_PEN)        
        dc.DrawRectangle(0,0,dcW,dcH)
        
        if not self.parent.story: return
        
        dc.SetPen(wx.Pen((0,0,255),1))        
        timeDelta = float(self.end-self.begin)
        bounds = []
        for creation in self.parent.story.file_creations["video"]:
            if creation >= self.begin and creation <= self.end:
                pct = (creation-self.begin) / timeDelta
                left = pct*dcW
                bounds.append(left)

        i = 0
        for creation in self.parent.story.file_creations["video"]:
            if creation >= self.begin and creation < self.end:                
                thumb = self.thumbs[creation]
                maxwidth = bounds[i+1] - bounds[i]
                (desired_width,desired_height) = util.geometry.getScaledDimensions(thumb.GetSize(),(maxwidth,dcH))
                thumb = thumb.Scale(desired_width,desired_height,wx.IMAGE_QUALITY_NORMAL)            
                thumb = wx.BitmapFromImage(thumb)
                dc.DrawBitmap(thumb,bounds[i],0)
                dc.DrawLine(bounds[i],0,bounds[i],dcH)
                i+=1