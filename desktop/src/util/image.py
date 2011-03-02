'''
(c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

@author: Alex Levenson (alex@isnotinvain.com)

image utility functions for opencv images
'''
import cv
import Image
import geometry
import wx

def saveCvSubRect(path,img,rect):
    imgView = cv.GetSubRect(img, rect)
    cv.SaveImage(path, imgView)

def cvToWx(img):
    img = cv.CloneImage(img)
    cv.CvtColor(img, img, cv.CV_BGR2RGB)        
    return wx.ImageFromBuffer(img.width,img.height,img.tostring())

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