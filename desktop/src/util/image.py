'''
Raconteur (c) Alex Levenson 2011
All rights reserved

@author: Alex Levenson (alex@isnotinvain.com)

image utility functions for opencv images
'''

import cv
import geometry
import wx

def cvGrayCopy(img):
    gray = cv.CreateImage((img.width, img.height), img.depth, 1)
    cv.CvtColor(img, gray, cv.CV_RGB2GRAY)
    return gray

def getCvSubRect(img, rect):
    rect = tuple(map(int, rect))
    subView = cv.GetSubRect(img, rect)
    sub = cv.CreateImage(rect[2:4], img.depth, img.nChannels)
    cv.Copy(subView, sub)
    return sub

def saveImage(img, path, scaleTo=None):
    if scaleTo:
        scaled = cv.CreateImage(scaleTo, img.depth, img.nChannels)
        cv.Resize(img, scaled, cv.CV_INTER_LINEAR)
        img = scaled
    cv.SaveImage(path, img)

def cvToWx(img):
    img = cv.CloneImage(img)
    cv.CvtColor(img, img, cv.CV_BGR2RGB)
    return wx.ImageFromBuffer(img.width, img.height, img.tostring())

def cvScaleToSize(img, max_width, max_height, returnFactor=False):
    """
    @return a scaled copy of img that fits inside max_width,max_height
    """

    size, factor = geometry.getScaledDimensions((img.width, img.height), (max_width, max_height), True)
    size = map(int, size)

    scaled = cv.CreateImage(size, img.depth, img.nChannels)
    cv.Resize(img, scaled, cv.CV_INTER_LINEAR)
    if returnFactor:
        return scaled, factor
    return scaled

def cvDrawObjectBoundaries(img, objects, color=(255, 0, 0)):
    for (x, y, w, h), _ in objects:
        cv.Rectangle(img, (x, y), (x + w, y + h), color)
