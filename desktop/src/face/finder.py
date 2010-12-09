'''
(c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

@author: Alex Levenson (alex@isnotinvain.com)
'''

import sys
from opencv.cv import cvLoadHaarClassifierCascade, cvCreateImage, cvCvtColor, CV_BGR2GRAY, \
cvEqualizeHist, cvHaarDetectObjects, cvCreateMemStorage, cvSize, cvPoint, cvRectangle, \
CV_RGB

from opencv.highgui import cvCreateFileCapture, cvQueryFrame, \
cvCreateVideoWriter, CV_FOURCC, cvWriteFrame

import util.image

cascade_path = "haarcascades/haarcascade_frontalface_alt.xml"
cascade = cvLoadHaarClassifierCascade(cascade_path,(1,1))
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
    gray = cvCreateImage((img.width,img.height),8,1) 
    cvCvtColor(img,gray,CV_BGR2GRAY)
        
    cvEqualizeHist(gray,gray)
    
    # now the face detection
    faces_raw = cvHaarDetectObjects(gray,cascade,cvCreateMemStorage(),scale_factor, min_neighbors, flags, cvSize(*min_size))
    
    faces = []
    for face in faces_raw:
        f = FaceRect(face.x,face.y,face.width,face.height)
        faces.append(f)
    
    return faces

def draw_faces(img,faces):    
    for face_rect in faces:
        # blit rectangles for each face to the color img
        pt1 = cvPoint(face_rect.x,face_rect.y)
        pt2 = cvPoint(face_rect.x+face_rect.width,face_rect.y+face_rect.height)
        cvRectangle(img,pt1,pt2,CV_RGB(0,255,0),8,0)
    
    
if __name__ == "__main__":
    if not len(sys.argv) == 3: raise Exception("Requires 2 command line arguments, input file path and output file path")
    
    capture = cvCreateFileCapture(sys.argv[1])
    if not capture:
        raise Exception("Couldn't load file"+sys.argv[1])

    writer=cvCreateVideoWriter(sys.argv[2],CV_FOURCC('P','I','M','1'),30,cvSize(888,500),True)    

    while True:
        frame = cvQueryFrame(capture)
        if frame is None: break
        s = util.image.scale_to_size(frame,500,500)
        
        faces = find_faces(s,scale_factor=1.1, min_neighbors=3, flags=0, min_size=(100, 100))
        draw_faces(s,faces)
        cvWriteFrame(writer,frame)
    print "done!"