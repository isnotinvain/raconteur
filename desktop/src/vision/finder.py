'''
(c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

@author: Alex Levenson (alex@isnotinvain.com)
'''

import cv,os

class ObjectFinder(object):
    """
    Finds objects in images using openCV's HaarCascasde object detector
    """
    lastSlash = __file__.rfind("/")
    DEFAULT_CASCADE = os.path.join(__file__[0:lastSlash],"haarcascades/haarcascade_frontalface_alt.xml")  
    
    def __init__(self, cascade_path=DEFAULT_CASCADE):        
        try:
            self.cascade = cv.Load(cascade_path)
        except:
            raise Exception("Couldn't load cascade file: "+cascade_path)
    
    def findInImage(self,img,scale_factor=1.1, min_neighbors=3, flags=0, min_size=(10,10)):
        # TODO: is it worth it to convert to greyscale first?
                        
        objects = cv.HaarDetectObjects(img,self.cascade,cv.CreateMemStorage(),scale_factor, min_neighbors, flags,min_size)
        
        return objects