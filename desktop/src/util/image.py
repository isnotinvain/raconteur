'''
(c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

@author: Alex Levenson (alex@isnotinvain.com)
'''
from opencv import cvCreateImage,cvResize,CV_INTER_LINEAR

def scale_to_size(img,max_width,max_height):
    """
    @return a scaled copy of img that fits inside the box created by max_width and max_height, size it was scaled to    
    """
    wfactor,hfactor = 1,1
    
    if img.width > max_width: wfactor = float(max_width)/img.width
    if img.height > max_height: hfactor = float(max_height)/img.height

    factor = min(wfactor,hfactor)
    size = (int(img.width*factor),int(img.height*factor))
    scaled = cvCreateImage(size,img.depth,img.nChannels)
    cvResize(img,scaled,CV_INTER_LINEAR)
    return scaled,size