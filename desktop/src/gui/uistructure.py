import os
import cPickle
import wx
import cv
import widgets
import stream.story
import stream.importer
import vision.finder
import vision.tracker
import vision.recognizer
import videoOverlays
import util.filesystem

def checkStory(self,evnt=None):
    if not self.story:
        d = wx.MessageDialog(self,"You need to open a story first!","Wooops!",wx.OK)
        d.ShowModal()
        d.Destroy()
        return False
    return True

def onImport(self,event):
    if not checkStory(self): return    
    d = widgets.ImportDialog(self,wx.ID_ANY)
    if d.ShowModal()==wx.ID_OK:
        streamType = d.streamTypeCtrl.GetValue()        
        directory = d.directoryCtrl.GetValue()
        d.Destroy()
        imp = stream.importer.StreamImporter(streamType,self.story.path,d.moveCheck.GetValue())
        progDialog = wx.ProgressDialog("Importing","Importing...",maximum=1000,parent=self,style=wx.PD_CAN_ABORT)        
        try:            
            imp.importDirectory(directory,progDialog=progDialog)
        except stream.importer.NoSuchDirectoryError:
            widgets.misc.messageBox(self, "Directory does not exist:\n"+directory, "Woops!")
            progDialog.Destroy()
            return
        progDialog.Destroy()
        self.story.crawl(streamType)
        self.timelinePanel.loadThumbs()
        self.Refresh()
        self.Update()
    else: d.Destroy()
    
def onAnalyze(self,event):
    d = widgets.AnalyzeDialog(self,wx.ID_ANY)
    if d.ShowModal()==wx.ID_OK:
        faceFind = d.faceCheck.GetValue()
        if faceFind:
            faceScale = eval(d.faceScale.GetValue())
            faceParams = eval(d.faceParams.GetValue())
        
        faceTrack = d.trackCheck.GetValue()            
        if faceTrack:
            trackParams = eval(d.trackParams.GetValue())
        
        faceExtract = d.extractCheck.GetValue()
        if faceExtract:
            extractParams = eval(d.extractParams.GetValue())
            
        faceRecognize = d.recognizeCheck.GetValue()
        if faceRecognize:
            recognizeParams = eval(d.recognizeParams.GetValue())
                        
        d.Destroy()

        if faceFind:
            video = stream.video.Video(self.currentVideo)
            if faceScale:
                finder = vision.finder.ObjectFinder(scaleTo=faceScale)
            else:
                finder = vision.finder.ObjectFinder()
            progDialog = wx.ProgressDialog("Extracting Face Boundaries","Working...",maximum=1000,parent=self,style=wx.PD_CAN_ABORT)
            video.face_bounds = finder.findInVideo(self.videoPanel.video,progDialog=progDialog,**faceParams)
            video.writeFaceBounds()
            progDialog.Destroy()
            video = None
        
        if faceTrack:
            video = stream.video.Video(self.currentVideo)
            video.loadFaceBounds()
            tracker = vision.tracker.ObjectTracker(**trackParams)
            video.face_tracks = tracker.extractAndInerpolateTracks(video.face_bounds)
            video.writeFaceTracks()
            video = None
            
        if faceExtract:
            video = stream.video.Video(self.currentVideo)
            
            self.peoplePanel.pause()
            video.loadFaceBounds()
            video.loadFaceTracks()

            video.calcDuration()
            progDialog = wx.ProgressDialog("Extracting Faces","Working...",maximum=video.getNormalizedFrameCount(),parent=self,style=wx.PD_CAN_ABORT)
            faceGroups = vision.tracker.ObjectTracker.getFacesFromTracks(video,progDialog)
            progDialog.Destroy()
            
            numFaces = reduce(lambda x,y: x+y,map(len,faceGroups))
                        
            progDialog = wx.ProgressDialog("Saving Faces","Working...",maximum=numFaces,parent=self,style=wx.PD_CAN_ABORT)
            prog = 0
            root = os.path.join(self.story.getUnrecognizedPeopleDir(),video.creation)                
            util.filesystem.ensureDirectoryExists(root)
            for fl in os.listdir(root):
                os.remove(os.path.join(root,fl))
                
            for i,faceGroup in enumerate(faceGroups):
                filename = root+"/"+str(i)+".avi"
                writer = cv.CreateVideoWriter(filename, cv.CV_FOURCC('P', 'I', 'M', '1'), video.getFps(), extractParams['scaleTo'], True)
                for face in faceGroup:
                    cont,_ = progDialog.Update(prog,"Saving Faces")
                    if not cont: 
                        progDialog.Destroy()
                        video.reset()
                        return                                         
                    scaled = cv.CreateImage(extractParams['scaleTo'],face.depth,face.nChannels)
                    cv.Resize(face,scaled,cv.CV_INTER_LINEAR)
                    cv.WriteFrame(writer, scaled)
                    prog+=1
            progDialog.Destroy()
            self.peoplePanel.loadPeople()
            video = None

def onShowOverlays(self,event):
    bounds = False
    tracks = False
    recognize = False
    
    video = stream.video.Video(self.currentVideo)
    try:
        video.loadFaceBounds()
        bounds = True
    except:
        pass
    
    try:
        video.loadFaceTracks()
        tracks = True
    except:
        pass
    
    d = widgets.ShowOverlaysDialog(self,wx.ID_ANY,bounds,tracks,recognize)
    if d.ShowModal()==wx.ID_OK:
        if bounds:
            bounds = d.faceCheck.GetValue()
        if tracks:
            tracks = d.trackCheck.GetValue()
        if recognize:
            recognize = d.extractCheck.GetValue()                    
        d.Destroy()
        
        self.videoPanel.overlays = []
        
        if bounds:
            overlay = videoOverlays.overlayFromFaceBounds(video.face_bounds)
            self.videoPanel.overlays.append(overlay)
        if tracks:
            overlay = videoOverlays.overlayFromTracks(video.face_tracks,video.face_bounds)
            self.videoPanel.overlays.append(overlay)
        
        video = None
    else: d.Destroy()
    
def onNewStory(self,event):
    d = widgets.NewStoryDialog(self,wx.ID_ANY)
    if d.ShowModal()==wx.ID_OK:
        path = d.directoryCtrl.GetValue()
        name = d.nameCtrl.GetValue()        
        story = stream.story.Story(name,path)
        story.save()
        self.loadStory(path)            
    d.Destroy()

def onOpenStory(self,event):
    d = wx.DirDialog(self, message="Open A Story",style = wx.DD_DEFAULT_STYLE|wx.DD_DIR_MUST_EXIST)
    if d.ShowModal() == wx.ID_OK:
        self.loadStory(d.GetPath())
    d.Destroy()
    
def onExit(self,event):
    self.Close()

def onAbout(self,event):
    d = wx.MessageDialog(self, self.ABOUT, "About Raconteur", wx.OK)
    d.ShowModal()
    d.Destroy()

def onPlayPause(self,event):
    self.videoPanel.playPause()

def onReset(self,event):
    self.videoPanel.pause()
    self.videoPanel.reset()    

def onTrain(self,event):
    ids = vision.recognizer.train(self.story.getPeopleDir())
    f = open(os.path.join(self.story.getPeopleDir(),".ids"),"w")
    cPickle.dump(ids,f)
    f.close()
    
tools = (
            ("Import", onImport),
            ("Analyze", onAnalyze),
            ("Train", onTrain),
            ("Overlays", onShowOverlays),
            ("Play",onPlayPause)
        )

menu =  (
            ("&File",    (
                            ("&New Story","Create a new story",onNewStory),
                            ("&Open Story","Open a new story",onOpenStory),
                            ("E&xit","Close Raconteur",onExit,wx.ID_EXIT),
                        )
            ),
            ("&Playback",    (
                            ("&Play / Pause","Play or Pause the current video",onPlayPause),
                            ("&Reset","Reset the current video",onReset),
                        )
            ),            
            ("&Help",    (
                            ("&About","About Raconteur",onAbout,wx.ID_ABOUT),
                        )
            ),
        )