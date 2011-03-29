import os
import cPickle
import cveigenface

    
def train(peopleDir):
    people = os.listdir(peopleDir)
    if "unrecognized" in people: people.remove("unrecognized")
    
    videos = {}
    for person in people:
        if person[0] == ".": continue
        videos[person] = []
        for f in os.listdir(os.path.join(peopleDir,person)):
            vid = os.path.join(peopleDir,person,f)
            videos[person].append(vid)
    
    peopleIDs = cveigenface.train(videos,os.path.join(peopleDir,".trainingData"))
    return peopleIDs

def recognize(peopleDir,video_path):
    f = open(os.path.join(peopleDir,".ids"),"r")
    ids = cPickle.load(f)
    f.close()
    
    id2name = dict((v,k) for k,v in ids.iteritems())
    
    recog = cveigenface.recognize(video_path,os.path.join(peopleDir,".trainingData"),True)
    
    hist = dict((v,0.0) for v in ids)
    total = 0.0
    for id,_ in recog:
        hist[id2name[id]] += 1
        total += 1
    
    for k in hist:
        hist[k] /= total
    
    return hist,total