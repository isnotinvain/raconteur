import wx
import widgets
import stream.story
import vision.finder
import vision.tracker
import videoOverlays

def checkStory(self,evnt=None):
    if not self.story:
        d = wx.MessageDialog(self,"You need to open a story first!","Wooops!",wx.OK)
        d.ShowModal()
        d.Destroy()
        return False
    return True

def onImport(self,event):
    print "import"
    
def onAnalyze(self,event):
    d = widgets.AnalyzeDialog(self,wx.ID_ANY)
    if d.ShowModal()==wx.ID_OK:
        faceFind = d.faceCheck.GetValue()
        faceScale = eval(d.faceScale.GetValue())
        faceParams = eval(d.faceParams.GetValue())
        faceTrack = d.trackCheck.GetValue()            
        trackParams = eval(d.trackParams.GetValue())
        
        faceRecognize = d.recognizeCheck.GetValue()
        #recognizeParams = eval(d.recognizeParams.GetValue())
        d.Destroy()

        if faceFind:
            self.currentVideo.reset()
            if faceScale:
                finder = vision.finder.ObjectFinder(scaleTo=faceScale)
            else:
                finder = vision.finder.ObjectFinder()
            progDialog = wx.ProgressDialog("Extracting Face Boundaries","Working...",maximum=1000,parent=self,style=wx.PD_CAN_ABORT)
            self.currentVideo.face_bounds = finder.findInVideo(self.videoPanel.video,progDialog=progDialog,**faceParams)
            self.currentVideo.writeFaceBounds()
            progDialog.Destroy()
        else: return
        
        if faceTrack:
            tracker = vision.tracker.ObjectTracker()
            self.currentVideo.face_tracks = tracker.extractAndInerpolateTracks(self.currentVideo.face_bounds)
            self.currentVideo.writeFaceTracks()
        else: return
        
        if faceRecognize:
            pass
        else: return
                
        d.Destroy()

def onShowOverlays(self,event):
    bounds = False
    tracks = False
    recognize = False
        
    try:
        self.currentVideo.loadFaceBounds()
        bounds = True
    except:
        pass
    
    try:
        self.currentVideo.loadFaceTracks()
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
            recognize = d.recognizeCheck.GetValue()                    
        d.Destroy()
        
        self.videoPanel.overlays = []
        
        if bounds:
            overlay = videoOverlays.overlayFromFaceBounds(self.currentVideo.face_bounds)
            self.videoPanel.overlays.append(overlay)
        if tracks:
            overlay = videoOverlays.overlayFromTracks(self.currentVideo.face_tracks,self.currentVideo.face_bounds)
            self.videoPanel.overlays.append(overlay)
                
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
    d = widgets.OpenStoryDialog(self,wx.ID_ANY)
    if d.ShowModal()==wx.ID_OK:
        self.loadStory(d.directoryCtrl.GetValue())
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
    self.videoPanel.reset()
    
tools = (
            ("Import", onImport),
            ("Analyze", onAnalyze),
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