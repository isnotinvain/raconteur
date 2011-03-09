import os
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
        self.raw_files = {}        
        self.file_creations = {}

    def save(self):
        util.filesystem.ensureDirectoryExists(self.path)
        f = open(os.path.join(self.path,".raconteur"),"w")
        cPickle.dump(self,f)
        f.close()

        
    def crawl(self,streamType):
        """
        finds all files of a particular stream type
        """
        self.raw_files[streamType] = {}        
        for root, _, files in os.walk(self.path):            
            if root[root.rfind("/")+1:] == streamType:
                for file in files:
                    if file[0] == ".": continue
                    creation_stamp = int(file[:file.rfind('.')])
                    self.raw_files[streamType][creation_stamp] = os.path.join(root,file)
        
        self.file_creations[streamType] = sorted(self.raw_files)