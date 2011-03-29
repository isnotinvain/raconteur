'''
Created on Feb 3, 2011

@author: Alex Levenson (alex@isnotinvain.com)
'''
import os
import shutil

import wx
import util.filesystem
from widgets import ManageAFaceDialog
import video
import vision.video

class PeoplePanel(video.VideoStack):

    def onLoad(self,event):
        d=ManageAFaceDialog(self,wx.ID_ANY,event.path)
        action = d.ShowModal()
        if action == ManageAFaceDialog.ADD_FACE:
            name = d.nameCtrl.GetValue()
            dest = self.parent.story.getPersonDir(name)
            util.filesystem.ensureDirectoryExists(dest)
            dest = os.path.join(dest,util.filesystem.generateUniqueFileName(dest,".avi"))
            shutil.move(event.path,dest)
            self.clear()
            self.loadThumbs(self.crawlUnrecognized())
        elif action == ManageAFaceDialog.DEL_FACE:
            self.clear()
            os.remove(event.path)
            self.loadThumbs(self.crawlUnrecognized())
        elif action == ManageAFaceDialog.RECOG_FACE:
            hist = vision.recognizer.recognize(self.parent.story.getPeopleDir(), event.path)
            print hist
        d.Destroy()

        self.clear()
        self.loadThumbs(self.crawlUnrecognized())

    def crawlUnrecognized(self):
        peopleDir = os.path.join(self.parent.story.getUnrecognizedPeopleDir(),vision.video.CvVideo.getCreation(self.parent.currentVideo))
        if os.path.exists(peopleDir):
            faceVideos = []
            for v in os.listdir(peopleDir):
                if v[0] == ".": continue
                faceVideos.append(os.path.join(peopleDir,v))
        else:
            faceVideos = []

        return faceVideos