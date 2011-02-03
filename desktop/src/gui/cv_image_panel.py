'''
Created on Feb 3, 2011

@author: Alex Levenson (alex@isnotinvain.com)
'''
import wx
import cv
from util import image
class CvImagePanel(wx.Panel):
    '''
    A panel that can draw openCV images inside itself
    '''
    def __init__(self,parent,id,**kwargs):
        wx.Panel.__init__(self,parent,id,**kwargs)
        self.image = None
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_SIZE, self.onPaint)
    
    def set_image(self,wxImage):
        self.image = wxImage
    
    def set_cv_image(self,img):
        img = cv.CloneImage(img)
        cv.CvtColor(img, img, cv.CV_BGR2RGB)
        #bmp = wx.BitmapFromBuffer(img.width,img.height,img.tostring())        
        self.set_image(wx.ImageFromBuffer(img.width,img.height,img.tostring()))
    
    def onPaint(self,event):
        dc = wx.PaintDC(self)
        dc.Clear()
        self.draw_image(dc)    
    def draw_image(self,dc):
        desired_width,desired_height = image.get_scale_dimensions(self.image.GetSize(), dc.GetSize())
        img = self.image.Scale(desired_width,desired_height,wx.IMAGE_QUALITY_HIGH)
        bmp = wx.BitmapFromImage(img)
        dc.DrawBitmap(bmp,0,0)
        