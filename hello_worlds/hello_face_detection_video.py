"""
Alex Levenson
Raconteur

Hello World equivalent of face detection using opencv (on a video stream)

Can be run as a script: hello_face_detection_video.py
"""

import sys
from opencv.cv import *
from opencv.highgui import *

cascade_path = "/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml"
cascade = cvLoadHaarClassifierCascade(cascade_path,(1,1))
if not cascade:
	raise Exception("Couldn't load classifier file")

def find_faces(img,scale_factor=1.85, min_neighbors=3, flags=0, min_size=(30, 30)):	
	
	# create a grayscale copy for the classifier to work on
	gray = cvCreateImage((img.width,img.height),8,1) 
	cvCvtColor(img,gray,CV_BGR2GRAY)
		
	cvEqualizeHist(gray,gray)
	
	# now the face detection
	faces = cvHaarDetectObjects(gray,cascade,cvCreateMemStorage(),scale_factor, min_neighbors, flags, cvSize(*min_size))
	
	return faces

def draw_faces(img,faces):
	for face_rect in faces:
		# blit rectangles for each face to the color img
		pt1 = cvPoint(face_rect.x,face_rect.y)
		pt2 = cvPoint(face_rect.x+face_rect.width,face_rect.y+face_rect.height)
		cvRectangle(img,pt1,pt2,CV_RGB(0,255,0),8,0)
	
if __name__ == "__main__":
	capture = cvCreateCameraCapture(0)	
	if not capture:
		raise Exception("Couldn't get your camera...")

	#writer=cvCreateVideoWriter("out.avi",CV_FOURCC('P','I','M','1'),30,cvSize(640,480),True)
				
	cvNamedWindow("Camera Face Detection")
	while True:
		frame = cvQueryFrame(capture)
		if frame is None: break
		
		faces = find_faces(frame,scale_factor=1.1, min_neighbors=3, flags=0, min_size=(100, 100))
		draw_faces(frame,faces)
		cvShowImage("Camera Face Detection",frame)
	#	cvWriteFrame(writer,frame)
		k = cvWaitKey(10)
		if k == '\x1b': break
