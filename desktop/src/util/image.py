'''
(c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

@author: Alex Levenson (alex@isnotinvain.com)

image utility functions for opencv images
'''
import cv
import Image
import pygame

def cv_to_pygame(img):
    cv.CvtColor(img, img, cv.CV_BGR2RGB)
    pil = Image.fromstring("RGB", cv.GetSize(img), img.tostring())            
    py_img = pygame.image.frombuffer(pil.tostring(), pil.size, pil.mode)
    return py_img

def scale_to_size(img,max_width,max_height):
    """
    @return a scaled copy of img that fits inside the box created by max_width and max_height, size it was scaled to    
    """
    wfactor,hfactor = 1,1
    
    if img.width > max_width: wfactor = float(max_width)/img.width
    if img.height > max_height: hfactor = float(max_height)/img.height

    factor = min(wfactor,hfactor)
    size = (int(img.width*factor),int(img.height*factor))
    scaled = cv.CreateImage(size,img.depth,img.nChannels)
    cv.Resize(img,scaled,cv.CV_INTER_LINEAR)
    return scaled,size