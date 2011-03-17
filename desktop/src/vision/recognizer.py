import os
import cPickle
import cveigenface

def train(peopleDir):
    people = os.listdir(peopleDir)
    if "unrecognized" in people: people.remove("unrecognized")
    
    videos = {}
    
    for person in people:
        videos[person] = []
        for f in os.listdir(os.path.join(peopleDir,person)):
            vid = os.path.join(peopleDir,person,f)
            videos[person].append(vid)
    
    peopleIDs = cveigenface.train(videos,os.path.join(peopleDir,".trainingData"))
    return peopleIDs

def recognize(peopleDir,video):
    f = open(os.path.join(peopleDir,".ids"),"r")
    ids = cPickle.load(f)    
    f.close()
    recog = cveigenface.recognize(video.file_path,os.path.join(peopleDir,".trainingData"))
    hist = dict((v,0.0) for v in ids.itervalues())    
    total = 0.0
    for id in recog:
        hist[ids[id]] += 1
        total += 1
    
    for k in hist:
        hist[k] /= total
    
    return hist,total