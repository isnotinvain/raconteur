'''
Raconteur (c) Alex Levenson 2011
All rights reserved

@author: Alex Levenson (alex@isnotinvain.com)

Face Recognition, relies on cveigenface.c
which does all the real work. It's a cpython 
file I wrote that uses opencv's c API because
pyopencv doesn't support eigenfaces
'''

import os
import cPickle
import cveigenface
import util.filesystem

def train(peopleDir, skipNFrames=10):
    people = os.listdir(peopleDir)
    if "unrecognized" in people: people.remove("unrecognized")

    videos = {}
    for person in people:
        if person[0] == ".": continue
        videos[person] = []
        for f in os.listdir(os.path.join(peopleDir, person)):
            vid = os.path.join(peopleDir, person, f)
            videos[person].append(vid)

    util.filesystem.ensureDirectoryExists(os.path.join(peopleDir, ".trainingData"))
    util.filesystem.ensureDirectoryExists(os.path.join(peopleDir, ".trainingData", "eigenFaces"))
    peopleIDs = cveigenface.train(videos, os.path.join(peopleDir, ".trainingData"), skipNFrames)
    return peopleIDs

def recognize(peopleDir, video_path, useEuclidean=True):
    f = open(os.path.join(peopleDir, ".trainingData", ".ids"), "r")
    ids = cPickle.load(f)
    f.close()

    id2name = dict((v, k) for k, v in ids.iteritems())

    recog = cveigenface.recognize(video_path, os.path.join(peopleDir, ".trainingData"), useEuclidean)

    hist = dict((v, 0.0) for v in ids)
    total = 0.0
    for id, _ in recog:
        hist[id2name[id]] += 1
        total += 1

    for k in hist:
        hist[k] /= total

    return hist, total
