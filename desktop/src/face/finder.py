'''
(c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

@author: Alex Levenson (alex@isnotinvain.com)
'''

import sys
import cv
import util.image

class HaarFinder(object):
    def __init__(self, cascade_path):
        try:
            self.cascade = cv.Load(cascade_path)
        except:
            raise Exception("Couldn't load cascade file: "+cascade_path)
    
    def find_in_image(self,img,scale_factor=1.85, min_neighbors=3, flags=0, min_size=(30, 30)):
        # create a grayscale copy for the classifier to work on
        #gray = cv.CreateImage((img.width,img.height),8,1) 
        #cv.CvtColor(img,gray,cv.CV_BGR2GRAY)
        
        # now the object detection
        objects = cv.HaarDetectObjects(img,self.cascade,cv.CreateMemStorage(),scale_factor, min_neighbors, flags,min_size)
        
        return objects
    
    def draw_object_boundaries(self,img,objects,color=(255,0,0)):        
        for (x,y,w,h),_ in objects:
            cv.Rectangle(img, (x,y), (x+w,y+h), color)
            
if __name__ == "__main__":
    if len(sys.argv) < 2: raise Exception("Requires at least one argument: <input file> <optional output file>")
    
    capture = cv.CreateFileCapture(sys.argv[1])
    if not capture:
        raise Exception("Couldn't load file"+sys.argv[1])

    frame = cv.QueryFrame(capture)
    if frame is None: sys.exit()
    
    s_frame,s_frame_size = util.image.scale_to_size(frame, 500,500)
       
    writer = None
    if len(sys.argv) >= 3:
        writer=cv.CreateVideoWriter(sys.argv[2],
                                      #cv.GetCaptureProperty(capture,cv.CV_CAP_PROP_FOURCC), \
                                      cv.CV_FOURCC('P','I','M','1'), \
                                      cv.GetCaptureProperty(capture,cv.CV_CAP_PROP_FPS), \
                                      s_frame_size, \
                                      True)
    else:
        cv.NamedWindow("Object Detection")
    
    face_finder = HaarFinder("haarcascades/haarcascade_frontalface_alt.xml")
    
    while frame is not None:                      
        s_frame,s_frame_size = util.image.scale_to_size(frame, 500,500)
        objects = face_finder.find_in_image(s_frame,scale_factor=1.1, min_neighbors=3, flags=0, min_size=(10,10))
        face_finder.draw_object_boundaries(s_frame, objects)
        
        if writer:
            cv.WriteFrame(writer,s_frame)
            print cv.GetCaptureProperty(capture,cv.CV_CAP_PROP_POS_AVI_RATIO)*100          
        else:
            cv.ShowImage("Object Detection",s_frame)
            k = cv.WaitKey(10)
            if k == '\x1b': break
        
        frame = cv.QueryFrame(capture)
    print "done!"