'''
Created on Feb 3, 2011

@author: Alex Levenson (alex@isnotinvain.com)
'''
import wx
import cv
from util import image
from stream.video import Video

class CvVideoPanel(wx.Panel):
    '''
    A panel that can draw openCV images inside itself
    '''
    TIMER_ID = 0

    def __init__(self,parent,id,**kwargs):
        wx.Panel.__init__(self,parent,id,**kwargs)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_SIZE, self.onPaint)
        self.video = None
        self.current_frame = None
        self.current_frame_bmp = None
        self.old_size = None        
        self.timer = wx.Timer(self, self.TIMER_ID)
        self.timer_tick = None        
        self.Bind(wx.EVT_TIMER,self.on_next_frame)
        
        
        self.load_video("/home/alex/Desktop/blarg.avi")
    
    def load_video(self,path):
        self.video = Video(path)
        self.current_frame = self._convert_cv_image(self.video.getNextFrame())
        self.timer_tick = 1000/self.video.get_fps()
        if self.timer_tick == 0: self.timer_tick = 1000/30
        
    def play(self):
        self.timer.Start(self.timer_tick)
        
    def pause(self):
        self.timer.Stop()
    
    def on_next_frame(self,event):
        self.current_frame = self._convert_cv_image(self.video.getNextFrame())
        self.Refresh()
            
    def _convert_cv_image(self,img):
        img = cv.CloneImage(img)
        cv.CvtColor(img, img, cv.CV_BGR2RGB)        
        return wx.ImageFromBuffer(img.width,img.height,img.tostring())
    
    def onPaint(self,event):
        dc = wx.PaintDC(self)
        dcW,dcH = dc.GetSize()
        if dcW < 0 or dcH < 0: return
        
        dc.Clear()
        self.draw_current_frame(dc)

    def draw_current_frame(self,dc):
        if not self.old_size:
            self.old_size = dc.GetSize()
        if not self.current_frame_bmp or self.old_size != dc.GetSize():            
            desired_width,desired_height = image.get_scale_dimensions(self.current_frame.GetSize(), dc.GetSize())            
            img = self.current_frame.Scale(desired_width,desired_height,wx.IMAGE_QUALITY_NORMAL)
            self.current_frame_bmp = wx.BitmapFromImage(img)
        dc.DrawBitmap(self.current_frame_bmp,0,0)