import sys
from opencv.cv import *
from opencv.highgui import *

def find_face(img):	
	cvNamedWindow("Hello Face Detection")
	cvShowImage("Hello Face Detection",img)
	cvWaitKey()
	
if __name__ == "__main__":
	if len(sys.argv) != 2:
		raise Exception("Requires exactly 1 argument")
	img = cvLoadImage(sys.argv[1],CV_LOAD_IMAGE_UNCHANGED)
	find_face(img)