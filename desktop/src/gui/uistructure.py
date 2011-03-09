import wx
import widgets
import stream.story

def onImport(self,event):
    print "import"
    
def onAnalyze(self,event):
    print "analyze"

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
    pass

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
            ("Analyze", onAnalyze)
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