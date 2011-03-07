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


static int loadTrainingImages(PyObject* dataDict, IplImage*** faces, int* numFaces,CvMat** truth);
static void doTraining(IplImage** faces,int numFaces,IplImage*** eigenVectors, IplImage** avgTrainingImg, CvMat** eigenValues, CvMat** projection);
static void storeTrainingData(char* outFile, int nEigens, int numFaces, CvMat* truth, CvMat* eigenValues, CvMat* projection, IplImage* avgTrainingImg, IplImage** eigenVectors);
static int loadTestImages(PyObject* testFacePaths, IplImage*** faces, int* numFaces);
static int loadTrainingData(char* dataFilePath, int* nEigens,int* nTrainFaces, CvMat** truth, CvMat** eigenValues, CvMat** projection, IplImage** avgTrainingImg, IplImage*** eigenVectors);
int findNearestNeighbor(float* projectedTestFace, int nTrainFaces, int nEigens, CvMat* trainProjection);


static PyObject* FileLoadError;

// train(self,data,outFile)
// data is a list where the ith element is a list containt person I's training image paths
static PyObject *
cveigenface_train(PyObject *self, PyObject *args) {
    PyObject* dataNestedList;
    char* outFile;
    IplImage** faces = 0;
    CvMat* truth;
    int numFaces = 0;
    IplImage** eigenVectors=0;
    IplImage* avgTrainingImg=0;
    CvMat* eigenValues=0;
    CvMat* projection = 0;
	int success;

    if(!PyArg_ParseTuple(args, "Os", &dataNestedList, &outFile)) return NULL;

    success = loadTrainingImages(dataNestedList,&faces,&numFaces,&truth);
    if(!success) {
    	PyErr_SetString(FileLoadError, "Couldn't load a training image file\n");
		return NULL;
    }
    
    doTraining(faces, numFaces, &eigenVectors, &avgTrainingImg, &eigenValues,&projection);
    storeTrainingData(outFile,numFaces-1, numFaces, truth, eigenValues, projection, avgTrainingImg, eigenVectors);
    
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
cveigenface_recognize(PyObject *self, PyObject *args) {    
    PyObject *testFacePaths;   
    Py_ssize_t numTestFaces;
    int success,nEigens, nTrainFaces;
    CvMat *truth, *eigenValues, *trainProjection;
    IplImage *avgTrainingImg, **eigenVectors, **faces; 
    char* dataFilePath;
    float* projectedTestFace;
    int i;
    
    PyObject* recognition;
    
    if(!PyArg_ParseTuple(args, "Os", &testFacePaths,&dataFilePath)) return NULL;
    
    success = loadTestImages(testFacePaths,&faces,&numTestFaces);
    if(!success) {
    	PyErr_SetString(FileLoadError, "Couldn't load a test image file\n");
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

static int loadTrainingImages(PyObject* dataNestedList, IplImage*** faces, int* numFaces, CvMat** truth) {
    PyObject *personImagesList;
    int person,i,numPeople;
    int faceIndex = 0;
    
    *numFaces = 0;
    numPeople = (int) PyList_Size(dataNestedList);
    for(person=0;person<numPeople;person++) {
    	(*numFaces) += (int) PyList_Size(PyList_GetItem(dataNestedList,person));
    }

	*faces = (IplImage **)cvAlloc((*numFaces)*sizeof(IplImage *));
    *truth = cvCreateMat(1,*numFaces,CV_32SC1);
    
    for(person=0;person<numPeople;person++) {
        char *filePath;
        PyObject* personImagesList = PyList_GetItem(dataNestedList,person);
        Py_ssize_t len = PyList_Size(personImagesList);
        for(i=0;i<len;i++) {
            filePath = PyString_AsString(PyList_GetItem(personImagesList,i));
       		(*faces)[faceIndex] = cvLoadImage(filePath, CV_LOAD_IMAGE_GRAYSCALE);       		
            if(!(*faces)[faceIndex]) return 0;
            *((*truth)->data.i+faceIndex) = person;
            faceIndex++;
        }
    }
    return 1;
}

static int loadTestImages(PyObject* testFacePaths, IplImage*** faces, int* numTestFaces) {
	int i;
	char* filePath;
	
	*numTestFaces = PyList_Size(testFacePaths);
	
	*faces = (IplImage **)cvAlloc((*numTestFaces)*sizeof(IplImage *));
		
	for(i=0;i<*numTestFaces;i++) {
		filePath = PyString_AsString(PyList_GetItem(testFacePaths,i));
		(*faces)[i] = cvLoadImage(filePath, CV_LOAD_IMAGE_GRAYSCALE);
		if(!(*faces)[i]) return 0;
	}
	
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

static void doTraining(IplImage** faces,int numFaces,IplImage*** eigenVectors, IplImage** avgTrainingImg, CvMat** eigenValues, CvMat** projection) {
	int i,nEigens,offset;
	CvTermCriteria calcLimit;
	CvSize faceImgSize;

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
