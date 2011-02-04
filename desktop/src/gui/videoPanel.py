'''
Created on Feb 3, 2011

@author: Alex Levenson (alex@isnotinvain.com)
'''
import wx
import util.geometry
import util.image
from stream.video import Video

class VideoPanel(wx.Panel):
    '''
    A panel that can draw a video inside itself
    '''
    TIMER_ID = 0
    def __init__(self,parent,id,**kwargs):
        wx.Panel.__init__(self,parent,id,**kwargs)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_SIZE, self.onPaint)
        self.video = None
        self.cv_frame = None
        self.current_frame = None
        self.current_frame_bmp = None
        self.old_size = None        
        self.timer = wx.Timer(self, self.TIMER_ID)
        self.timer_tick = None        
        self.Bind(wx.EVT_TIMER,self.onNextFrame)
        self.overlays = []
    
    def loadVideo(self,path):
        self.video = Video(path)
        self.cv_frame = self.video.getNextFrame()
        self.current_frame = util.image.cvToWx(self.cv_frame)
        self.timer_tick = 1000/self.video.getFps()
        if self.timer_tick == 0: self.timer_tick = 1000/30
        self.onNextFrame(None)
        
    def play(self):
        if not self.video:
            raise Exception("You must call loadVideo first!")
        self.timer.Start(self.timer_tick)
        
    def pause(self):
        self.timer.Stop()
    
    def onNextFrame(self,event):
        self.cv_frame = self.video.getNextFrame()
        if not self.cv_frame:
            self.video.reset()
            self.pause()
            self.cv_frame = self.video.getNextFrame()            
        self.current_frame = util.image.cvToWx(self.cv_frame)
        self.Refresh()
    
    def onPaint(self,event):
        dc = wx.PaintDC(self)
        dcW,dcH = dc.GetSize()
        if dcW < 0 or dcH < 0: return
        
        dc.Clear()
        if self.video:
            self.drawCurrentFrame(dc)
            for overlay in self.overlays:                
                overlay(dc,self.video.getFrameNum())

    def drawCurrentFrame(self,dc):
        if not self.old_size:
            self.old_size = dc.GetSize()
        if not self.current_frame_bmp or self.old_size != dc.GetSize():            
            (desired_width,desired_height),factor = util.geometry.getScaledDimensions(self.current_frame.GetSize(), dc.GetSize(),True)
            dc.raconteurScaleFactor = factor
            img = self.current_frame.Scale(desired_width,desired_height,wx.IMAGE_QUALITY_NORMAL)
            self.current_frame_bmp = wx.BitmapFromImage(img)
        dc.DrawBitmap(self.current_frame_bmp,0,0)