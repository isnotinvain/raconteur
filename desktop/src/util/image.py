'''
(c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

@author: Alex Levenson (alex@isnotinvain.com)

image utility functions for opencv images
'''
import cv
import Image
import pygame
import geometry
import wx

def cvToWx(img):
    img = cv.CloneImage(img)
    cv.CvtColor(img, img, cv.CV_BGR2RGB)        
    return wx.ImageFromBuffer(img.width,img.height,img.tostring())

def cvToPygame(img):
    """
    @return an image that can be used in pygame
    """
    cv.CvtColor(img, img, cv.CV_BGR2RGB)
    pil = Image.fromstring("RGB", cv.GetSize(img), img.tostring())            
    py_img = pygame.image.frombuffer(pil.tostring(), pil.size, pil.mode)
    return py_img

def cvScaleToSize(img,max_width,max_height):
    """
    @return a scaled copy of img that fits inside max_width,max_height    
    """
    
    size = map(int, geometry.getScaledDimensions((img.width,img.height),(max_width,max_height)))

    scaled = cv.CreateImage(size,img.depth,img.nChannels)
    cv.Resize(img,scaled,cv.CV_INTER_LINEAR)
    return scaled

def cvDrawObjectBoundaries(img,objects,color=(255,0,0)):        
    for (x,y,w,h),_ in objects:
        cv.Rectangle(img, (x,y), (x+w,y+h), color)

def wxDrawObjecBoundaries(dc,bounds,color=(0,255,0)):
    dc.SetPen(wx.Pen(color, 1))
    dc.SetBrush(wx.Brush((0,0,0),style=wx.TRANSPARENT))
    for (x,y,w,h),_ in bounds:
        dc.DrawRectangle(x,y,w,h)