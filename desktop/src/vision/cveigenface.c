/*
    Alex Levenson (alex@isnotinvain)
    3/4/2011

    Eigenfaces implementation in cpython using opencv

    Shamelessly based on (in large part copied from) a tutorial by Robin Hewitt in 2007
    which can be found here:
    http://www.cognotics.com/opencv/servo_2007_series/part_5/index.html
    Article originally appeared in SERVO Magazine
    Tutorial was posted without a license, if you wish me to take down this
    file please let me know: alex@isnotinvain.com    

*/

#include <Python.h>
#include "cv.h"
#include "cvaux.h"
#include "highgui.h"


static int loadTrainingImages(PyObject* dataDict, IplImage*** faces, int* numFaces,CvMat** truth, PyObject** peopleIDs);

static void doTraining(IplImage** faces,int numFaces,IplImage*** eigenVectors, IplImage** avgTrainingImg, CvMat** eigenValues, CvMat** projection);

static void storeTrainingData(char* outFile, int nEigens, int numFaces, CvMat* truth, CvMat* eigenValues, CvMat* projection, IplImage* avgTrainingImg, IplImage** eigenVectors);

static int loadTestImages(char* testVideo, IplImage*** faces, int* numFaces);

static int loadTrainingData(char* dataFilePath, int* nEigens,int* nTrainFaces, CvMat** truth, CvMat** eigenValues, CvMat** projection, IplImage** avgTrainingImg, IplImage*** eigenVectors);

int findNearestNeighbor(float* projectedTestFace, int nTrainFaces, int nEigens, CvMat* trainProjection);

int faceGetter(int index, void* buffer, void* user_data);

static PyObject* FileLoadError;

// train(self,data,outFile)
// data is a dictionary mapping personID to a list of video files, outFile a string
static PyObject *
cveigenface_train(PyObject *self, PyObject *args) {
    PyObject *dataDict,*peopleIDs;
    char* outFile;
    IplImage** faces = 0;
    CvMat* truth;
    int numFaces = 0;
    IplImage** eigenVectors=0;
    IplImage* avgTrainingImg=0;
    CvMat* eigenValues=0;
    CvMat* projection = 0;
	int success;

    if(!PyArg_ParseTuple(args, "Os", &dataDict, &outFile)) return NULL;

    success = loadTrainingImages(dataDict,&faces,&numFaces,&truth,&peopleIDs);
    if(!success) {
    	PyErr_SetString(FileLoadError, "Couldn't load a training video file\n");
		return NULL;
    }
    
    doTraining(faces, numFaces, &eigenVectors, &avgTrainingImg, &eigenValues,&projection);
    storeTrainingData(outFile,numFaces-1, numFaces, truth, eigenValues, projection, avgTrainingImg, eigenVectors);
    
    return peopleIDs;
}

static PyObject *
cveigenface_recognize(PyObject *self, PyObject *args) {    
    Py_ssize_t numTestFaces;
    int success,nEigens, nTrainFaces;
    CvMat *truth, *eigenValues, *trainProjection;
    IplImage *avgTrainingImg, **eigenVectors, **faces; 
    char *testVideo,*dataFilePath;
    float* projectedTestFace;
    int i;
    
    PyObject *recognition;
    
    if(!PyArg_ParseTuple(args, "ss", &testVideo,&dataFilePath)) return NULL;
    
    success = loadTestImages(testVideo,&faces,&numTestFaces);
    if(!success) {
    	PyErr_SetString(FileLoadError, "Couldn't load a test video file\n");
		return NULL;
    }
    
    success = loadTrainingData(dataFilePath, &nEigens, &nTrainFaces, &truth, &eigenValues, &trainProjection, &avgTrainingImg, &eigenVectors);
    if(!success) {
    	PyErr_SetString(FileLoadError, "Couldn't load training data\n");
		return NULL;
    }
    
    recognition = PyTuple_New(numTestFaces);
    
	projectedTestFace = (float *)cvAlloc(nEigens*sizeof(float));
	for(i=0;i<numTestFaces;i++) {
		int iNearest, nearest;
		cvEigenDecomposite(
			faces[i],
			nEigens,
			eigenVectors,
			0, 0,
			avgTrainingImg,
			projectedTestFace);

		iNearest = findNearestNeighbor(projectedTestFace, nTrainFaces, nEigens, trainProjection);		
		nearest  = truth->data.i[iNearest];
		PyObject* pyNearest = Py_BuildValue("i",nearest);
		PyTuple_SetItem(recognition,i,pyNearest);
	}
    
    return recognition;
}

int findNearestNeighbor(float* projectedTestFace, int nTrainFaces, int nEigens, CvMat* trainProjection) {
	double leastDistSq = DBL_MAX;
	int i, iTrain, iNearest = 0;

	for(iTrain=0; iTrain<nTrainFaces; iTrain++)	{
		double distSq=0;

		for(i=0;i<nEigens;i++) {
			float d_i =
				projectedTestFace[i] -
				trainProjection->data.fl[iTrain*nEigens + i];
			//distSq += d_i*d_i / eigenValues->data.fl[i];  // Mahalanobis
			distSq += d_i*d_i; // Euclidean
		}

		if(distSq < leastDistSq) {
			leastDistSq = distSq;
			iNearest = iTrain;
		}
	}

	return iNearest;
}

static int loadTrainingImages(PyObject* dataDict, IplImage*** faces, int* numFaces, CvMat** truth, PyObject** peopleIDs) {
    PyObject *pyPath;
    char* path;
    int vid,numPeople=0,numVideos;
    int faceIndex = 0;
    IplImage* frame;    
    CvCapture* video;
    CvSize size;
    
    PyObject *key, *value;
	Py_ssize_t pos = 0;

	while (PyDict_Next(dataDict, &pos, &key, &value)) {
		numVideos = PyList_Size(value);
		for(vid=0;vid<numVideos;vid++) {
			pyPath = PyList_GetItem(value,vid);
			path = PyString_AsString(pyPath);
			video = cvCaptureFromFile(path);			
			(*numFaces) += cvGetCaptureProperty(video,CV_CAP_PROP_FRAME_COUNT)-1;
			cvReleaseCapture(&video);
		}
	}
    
	*faces = (IplImage **)cvAlloc((*numFaces)*sizeof(IplImage *));
    *truth = cvCreateMat(1,*numFaces,CV_32SC1);

    pos = 0;
	(*peopleIDs) = PyDict_New();
    while (PyDict_Next(dataDict, &pos, &key, &value)) {
		PyDict_SetItem((*peopleIDs),key,PyInt_FromLong(++numPeople));
		numVideos = PyList_Size(value);
		for(vid=0;vid<numVideos;vid++) {
			pyPath = PyList_GetItem(value,vid);
			path = PyString_AsString(pyPath);
			video = cvCaptureFromFile(path);
			frame = cvQueryFrame(video);
            if(frame!=NULL) {
                size.width = frame->width;
                size.height = frame->height;
			    while(frame != NULL) {
                    (*faces)[faceIndex] = cvCreateImage(size,frame->depth,1);
                    cvCvtColor(frame,(*faces)[faceIndex],CV_RGB2GRAY);
                    *((*truth)->data.i+faceIndex) = numPeople-1;
                    faceIndex++;
				    frame = cvQueryFrame(video);
			    }
            }
			cvReleaseCapture(&video);
		}
	}

    return 1;
}

static int loadTestImages(char* testVideo, IplImage*** faces, int* numTestFaces) {
    CvCapture *video;	
    IplImage* frame; 
    int faceIndex = 0;
    CvSize size; 

    video = cvCaptureFromFile(testVideo);
	(*numTestFaces) = cvGetCaptureProperty(video,CV_CAP_PROP_FRAME_COUNT)-1;
	
	*faces = (IplImage **)cvAlloc((*numTestFaces)*sizeof(IplImage *));

    frame = cvQueryFrame(video);
    if(frame!=NULL) {
        size.width = frame->width;
        size.height = frame->height;
        while(frame != NULL) {
            (*faces)[faceIndex] = cvCreateImage(size,frame->depth,1);
            cvCvtColor(frame,(*faces)[faceIndex],CV_RGB2GRAY);
            faceIndex++;
            frame = cvQueryFrame(video);
        }
    }

	cvReleaseCapture(&video);
	
	return 1;
}

static int loadTrainingData(char* dataFilePath, int* nEigens,int* nTrainFaces, CvMat** truth, CvMat** eigenValues, CvMat** projection, IplImage** avgTrainingImg, IplImage*** eigenVectors) {

	CvFileStorage * fileStorage;
	int i;
	fileStorage = cvOpenFileStorage(dataFilePath, 0, CV_STORAGE_READ);
	if(!fileStorage) return 0;

	*nEigens = cvReadIntByName(fileStorage, 0, "nEigens", 0);
	*nTrainFaces = cvReadIntByName(fileStorage, 0, "numFaces", 0);
	*truth = (CvMat *)cvReadByName(fileStorage, 0, "truth", 0);
	*eigenValues  = (CvMat *)cvReadByName(fileStorage, 0, "eigenValues", 0);
	*projection = (CvMat *)cvReadByName(fileStorage, 0, "projection", 0);
	*avgTrainingImg = (IplImage *)cvReadByName(fileStorage, 0, "avgTrainingImg", 0);
	*eigenVectors = (IplImage **)cvAlloc((*nTrainFaces)*sizeof(IplImage *));

	for(i=0;i<(*nEigens);i++) {
		char varname[200];
		sprintf(varname, "eigenVect_%d", i);
		(*eigenVectors)[i] = (IplImage *)cvReadByName(fileStorage, 0, varname, 0);
	}

	cvReleaseFileStorage( &fileStorage );
	return 1;
}

static void storeTrainingData(char* outFile, int nEigens, int numFaces, CvMat* truth, CvMat* eigenValues, CvMat* projection, IplImage* avgTrainingImg, IplImage** eigenVectors) {

	CvFileStorage * fileStorage;
	int i;
	fileStorage = cvOpenFileStorage(outFile, 0, CV_STORAGE_WRITE);
	cvWriteInt(fileStorage, "nEigens", nEigens);
	cvWriteInt(fileStorage, "numFaces", numFaces);
	cvWrite(fileStorage, "truth", truth, cvAttrList(0,0));
	cvWrite(fileStorage, "eigenValues", eigenValues, cvAttrList(0,0));
	cvWrite(fileStorage, "projection", projection, cvAttrList(0,0));
	cvWrite(fileStorage, "avgTrainingImg", avgTrainingImg, cvAttrList(0,0));
	for(i=0; i<nEigens; i++) {
		char varname[200];
		sprintf(varname, "eigenVect_%d", i);
		cvWrite(fileStorage, varname, eigenVectors[i], cvAttrList(0,0));
	}
	
	cvReleaseFileStorage(&fileStorage);
}

int faceGetter(int index, void* buffer, void* user_data) {
    memcpy(buffer,((IplImage**)(user_data))[index],((IplImage**)(user_data))[index]->nSize);
    return CV_NO_ERR;
}

static void doTraining(IplImage** faces,int numFaces,IplImage*** eigenVectors, IplImage** avgTrainingImg, CvMat** eigenValues, CvMat** projection) {
	int i,nEigens,offset;
	CvTermCriteria calcLimit;
	CvSize faceImgSize;
    CvInput getter;
    getter.callback = faceGetter;

	nEigens = numFaces-1;
    
	faceImgSize.width  = faces[0]->width;
	faceImgSize.height = faces[0]->height;

	*eigenVectors = (IplImage**)cvAlloc(sizeof(IplImage*) * nEigens);
	for(i=0; i<nEigens; i++)
		(*eigenVectors)[i] = cvCreateImage(faceImgSize, IPL_DEPTH_32F, 1);

	*eigenValues = cvCreateMat(1, nEigens, CV_32FC1);
	*avgTrainingImg = cvCreateImage(faceImgSize, IPL_DEPTH_32F, 1);

	calcLimit = cvTermCriteria( CV_TERMCRIT_ITER, nEigens, 1);


	// compute average image, eigenvalues, and eigenvectors
	cvCalcEigenObjects(
		numFaces,
     	(void*)faces,
		(void*)(*eigenVectors),
		CV_EIGOBJ_NO_CALLBACK,
		0,
        0,
		&calcLimit,
		*avgTrainingImg,
		(*eigenValues)->data.fl);

	cvNormalize(*eigenValues, *eigenValues, 1, 0, CV_L1, 0);

	*projection = cvCreateMat(numFaces, nEigens, CV_32FC1);
	offset = (*projection)->step / sizeof(float);
	for(i=0; i<numFaces; i++) {
		float pct = i; pct /= numFaces;
		printf("%f\n",pct);
		cvEigenDecomposite(
			faces[i],
			nEigens,
			*eigenVectors,
			0, 0,
			*avgTrainingImg,
			(*projection)->data.fl + i*offset);
	}
}


static PyMethodDef EigenfaceMethods[] = {
    {"train",  cveigenface_train, METH_VARARGS,
     "Create training data on a set of face images"},
     
     {"recognize",  cveigenface_recognize, METH_VARARGS,
     "Recognize a face given training data"},
     
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


PyMODINIT_FUNC
initcveigenface(void)
{
    PyObject* m = Py_InitModule("cveigenface", EigenfaceMethods);
    if(m==NULL) return;
    
    FileLoadError = PyErr_NewException("cveigenface.FileLoadError", NULL, NULL);
    Py_INCREF(FileLoadError);
    PyModule_AddObject(m, "FileLoadError", FileLoadError);
}
