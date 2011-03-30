'''
(c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

@author: Alex Levenson (alex@isnotinvain.com)
'''

import cv, os
from util.image import cvScaleToSize

class ObjectFinder(object):
    """
    Finds objects in images using openCV's HaarCascasde object detector
    """
    lastSlash = __file__.rfind("/")
    DEFAULT_CASCADE = os.path.join(__file__[0:lastSlash], "haarcascades/haarcascade_frontalface_alt.xml")

    def __init__(self, cascade_path=DEFAULT_CASCADE, scaleTo=None):
        try:
            self.cascade = cv.Load(cascade_path)
        except:
            raise Exception("Couldn't load cascade file: " + cascade_path)
        self.scaleTo = scaleTo

    def findInImage(self, img, scale_factor=1.1, min_neighbors=3, flags=0, min_size=(10, 10)):
        factor = 1.0
        if self.scaleTo:
            img, factor = cvScaleToSize(img, *self.scaleTo, returnFactor=True)

        #gray = cv.CreateImage((img.width,img.height), img.depth, 1)
        #cv.CvtColor(img, gray, cv.CV_RGB2GRAY)

        objects = cv.HaarDetectObjects(img, self.cascade, cv.CreateMemStorage(), scale_factor, min_neighbors, flags, min_size)

        if not factor == 1.0:
            scaledObjects = []
            for pts, n in objects:
                scaledObjects.append(((tuple(map(lambda x: x / factor, pts))), n))
            return scaledObjects

        return objects

    def findInVideo(self, video, scale_factor=1.1, min_neighbors=3, flags=0, min_size=(10, 10), progDialog=None):
        """
        Runs object detection on each frame of the video,
        this can be quite slow.
        """
        raw_bounds = []
        for frame in video.frames():
            raw = self.findInImage(frame, scale_factor, min_neighbors, flags, min_size)
            raw_bounds.append(raw)
            if progDialog:
                cont, _ = progDialog.Update(int(video.getRatio()*1000), "Extracting Face Boundaries...")
                if not cont: return raw_bounds
        return raw_bounds
