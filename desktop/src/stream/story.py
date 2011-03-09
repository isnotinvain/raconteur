import os
import bisect
import cPickle
import util

class Story(object):
    
    @classmethod
    def load(cls,path):
        f = open(os.path.join(path,".raconteur"),"r")
        story = cPickle.load(f)
        f.close()
        story.path = path
        return story
    
    def __init__(self,name,path):
        self.path = path
        self.name = name
        self.stream_files = {}        
        self.stream_creations = {}

    def save(self):
        util.filesystem.ensureDirectoryExists(self.path)
        f = open(os.path.join(self.path,".raconteur"),"w")
        cPickle.dump(self,f)
        f.close()
        
    def crawl(self,streamType):
        """
        finds all files of a particular stream type
        """
        self.stream_files[streamType] = {}        
        for root, _, files in os.walk(self.path):            
            if root[root.rfind("/")+1:] == streamType:
                for file in files:
                    if file[0] == ".": continue
                    creation_stamp = int(file[:file.rfind('.')])
                    self.stream_files[streamType][creation_stamp] = os.path.join(root,file)
        
        self.stream_creations[streamType] = sorted(self.stream_files[streamType])
                
    def getStreamsInRange(self,start,end,streamType):
        creations = self.stream_creations[streamType]
        s = bisect.bisect_right(creations,start)
        if s == len(creations): return []
        
        e = bisect.bisect_left(creations,end)
        if not e: return []
                
        return map(lambda x : (x,self.stream_files[streamType][x]),creations[s:e])