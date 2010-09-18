import sys
from opencv.cv import *
from opencv.highgui import *

cascade_path = "/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml"
cascade = cvLoadHaarClassifierCascade(cascade_path,(1,1))
if not cascade:
	raise Exception("Couldn't load classifier file")


def scale_to(img,max_width,max_height):
	wfactor,hfactor = 1,1
	
	if img.width > max_width: wfactor = float(max_width)/img.width
	if img.height > max_height: hfactor = float(max_height)/img.height

	factor = max(wfactor,hfactor)
	
		
	scaled = cvCreateImage((int(img.width*factor),int(img.height*factor)),img.depth,img.nChannels)
	cvResize(img,scaled,CV_INTER_LINEAR)
	return scaled	

def find_face(img,scale_factor=2, min_neighbors=3, flags=0, min_size=(30, 30)):	
	gray = cvCreateImage((img.width,img.height),8,1) 
	cvCvtColor(img,gray,CV_BGR2GRAY)
	gray = scale_to(gray,500,500)
	img = scale_to(img,500,500)
	cvEqualizeHist(gray,gray)
	faces = cvHaarDetectObjects(gray,cascade,cvCreateMemStorage(),scale_factor, min_neighbors, flags, cvSize(*min_size))
	for face_rect in faces:
		pt1 = cvPoint(face_rect.x,face_rect.y)
		pt2 = cvPoint(face_rect.x+face_rect.width,face_rect.y+face_rect.height)
		cvRectangle(img,pt1,pt2,CV_RGB(0,255,0),8,0)
			
	cvNamedWindow("Hello Face Detection")
	cvShowImage("Hello Face Detection",img)
	cvWaitKey()
	
if __name__ == "__main__":
	if len(sys.argv) != 2:
		raise Exception("Requires exactly 1 argument")

	img = cvLoadImage(sys.argv[1],CV_LOAD_IMAGE_UNCHANGED)
	print dir(img)
	find_face(img)