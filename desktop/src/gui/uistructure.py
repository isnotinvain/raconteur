import wx

def onImport(self,event):
    print "import"
    
def onAnalyze(self,event):
    print "analyze"

def onNewStory(self,event):
    pass

def onOpenStory(self,event):
    pass

def onExit(self,event):
    self.Close()

def onAbout(self,event):
    d = wx.MessageDialog(self, self.ABOUT, "About Raconteur", wx.OK)
    d.ShowModal()
    d.Destroy()
    
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
            ("&Help",    (
                            ("&About","About Raconteur",onAbout,wx.ID_ABOUT),
                        )
            ),
        )