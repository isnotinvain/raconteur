'''
(c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

@author: Alex Levenson (alex@isnotinvain.com)
'''

import sys
import opencv as cv

import opencv.highgui as hg

import util.image

cascade_path = "haarcascades/haarcascade_frontalface_alt.xml"
cascade = cv.cvLoadHaarClassifierCascade(cascade_path,(1,1))
if not cascade:
    raise Exception("Couldn't load classifier file")

class FaceRect(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height        

def find_faces(img,scale_factor=1.85, min_neighbors=3, flags=0, min_size=(30, 30)):    
    
    # create a grayscale copy for the classifier to work on
    gray = cv.cvCreateImage((img.width,img.height),8,1) 
    cv.cvCvtColor(img,gray,cv.CV_BGR2GRAY)
        
    #cv.cvEqualizeHist(gray,gray)
    
    # now the face detection
    faces_raw = cv.cvHaarDetectObjects(gray,cascade,cv.cvCreateMemStorage(),scale_factor, min_neighbors, flags, cv.cvSize(*min_size))
    
    faces = []
    for face in faces_raw:
        f = FaceRect(face.x,face.y,face.width,face.height)
        faces.append(f)
    
    return faces

def draw_faces(img,faces):    
    for face_rect in faces:
        # blit rectangles for each face to the color img
        pt1 = cv.cvPoint(face_rect.x,face_rect.y)
        pt2 = cv.cvPoint(face_rect.x+face_rect.width,face_rect.y+face_rect.height)
        cv.cvRectangle(img,pt1,pt2,cv.CV_RGB(0,255,0),8,0)
    
    
if __name__ == "__main__":
    if len(sys.argv) < 2: raise Exception("Requires at least one argument: <input file> <optional output file>")
    
    capture = hg.cvCreateFileCapture(sys.argv[1])
    if not capture:
        raise Exception("Couldn't load file"+sys.argv[1])

    frame = hg.cvQueryFrame(capture)    
    if frame is None: sys.exit()
    
    s_frame,s_frame_size = util.image.scale_to_size(frame, 500,500)
       
    writer = None
    if len(sys.argv) >= 3:
        writer=hg.cvCreateVideoWriter(sys.argv[2], \
                                      hg.CV_FOURCC('P','I','M','1'), #hg.cvGetCaptureProperty(capture,hg.CV_CAP_PROP_FOURCC), \
                                      hg.cvGetCaptureProperty(capture,hg.CV_CAP_PROP_FPS), \
                                      cv.cvSize(*s_frame_size), \
                                      True)
    else:
        hg.cvNamedWindow("Hello Face Detection")
    
    frame_count = 0
    total_frames = hg.cvGetCaptureProperty(capture,hg.CV_CAP_PROP_FRAME_COUNT)
    while frame is not None:                      
        s_frame,s_frame_size = util.image.scale_to_size(frame, 500,500)
        faces = find_faces(s_frame,scale_factor=1.1, min_neighbors=3, flags=0, min_size=(10,10))
        draw_faces(s_frame,faces)
        
        if writer:
            hg.cvWriteFrame(writer,s_frame)
            print frame_count / total_frames 
             
        else:
            hg.cvShowImage("Hello Face Detection",s_frame)
            k = hg.cvWaitKey(5)
            if k == '\x1b': break
        
        frame = hg.cvQueryFrame(capture)
        frame_count += 1
    hg.cvReleaseCapture(capture)
    print "done!"