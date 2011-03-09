'''
Created on Feb 3, 2011

@author: Alex Levenson (alex@isnotinvain.com)
'''

import wx

class NewStoryDialog(wx.Dialog):
    def __init__(self, parent, id,**kwargs):
        kwargs['title'] = "Create a New Story"
        wx.Dialog.__init__(self, parent, id,**kwargs)
        
        pvbox = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, wx.ID_ANY)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        dirLabel = wx.StaticText(panel,wx.ID_ANY,label="Enter a directory to store Raconteur's data:")        
        self.directoryCtrl = wx.TextCtrl(panel, wx.ID_ANY)
        
        nameLabel = wx.StaticText(panel,wx.ID_ANY,label="Enter a name for this story:")        
        self.nameCtrl = wx.TextCtrl(panel, wx.ID_ANY)
        
        pvbox.Add(dirLabel,0,wx.EXPAND)
        pvbox.Add(self.directoryCtrl,0,wx.EXPAND)
        pvbox.Add(nameLabel,0,wx.EXPAND)
        pvbox.Add(self.nameCtrl,0,wx.EXPAND)
        panel.SetSizer(pvbox)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, wx.ID_OK, "Create!") 
        hbox.Add(okButton, 1)        

        vbox.Add(panel)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        self.SetSizer(vbox)
        vbox.Fit(self)

class OpenStoryDialog(wx.Dialog):
    def __init__(self, parent, id,**kwargs):
        kwargs['title'] = "Open a Story"
        wx.Dialog.__init__(self, parent, id,**kwargs)
        
        pvbox = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, wx.ID_ANY)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        dirLabel = wx.StaticText(panel,wx.ID_ANY,label="Enter the path to the root of the story")        
        self.directoryCtrl = wx.TextCtrl(panel, wx.ID_ANY)
        
        
        pvbox.Add(dirLabel,0,wx.EXPAND)
        pvbox.Add(self.directoryCtrl,0,wx.EXPAND)
        panel.SetSizer(pvbox)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, wx.ID_OK, "Open") 
        hbox.Add(okButton, 1)        

        vbox.Add(panel)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        self.SetSizer(vbox)
        vbox.Fit(self)
        
class ImportDialog(wx.Dialog):
    def __init__(self, parent, id,**kwargs):
        kwargs['title'] = "Import to this Story"
        wx.Dialog.__init__(self, parent, id,**kwargs)
        
        pvbox = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, wx.ID_ANY)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        dirLabel = wx.StaticText(panel,wx.ID_ANY,label="Enter the path to the file / root of \nthe files you want to import")        
        self.directoryCtrl = wx.TextCtrl(panel, wx.ID_ANY)
        streamTypeLabel = wx.StaticText(panel,wx.ID_ANY,label="Enter the stream type \nex:(video, image, location, etc)")        
        self.streamTypeCtrl = wx.TextCtrl(panel, wx.ID_ANY)
        self.moveCheck = wx.CheckBox(panel,wx.ID_ANY,label="Move files instead of copy?")
        
        pvbox.Add(dirLabel,0,wx.EXPAND)
        pvbox.Add(self.directoryCtrl,0,wx.EXPAND)
        pvbox.Add(streamTypeLabel,0,wx.EXPAND)
        pvbox.Add(self.streamTypeCtrl,0,wx.EXPAND)
        pvbox.Add(self.moveCheck,0,wx.EXPAND)
        panel.SetSizer(pvbox)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, wx.ID_OK, "Import") 
        hbox.Add(okButton, 1)        

        vbox.Add(panel)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        self.SetSizer(vbox)
        vbox.Fit(self)
        
class AnalyzeDialog(wx.Dialog):
    def __init__(self, parent, id,**kwargs):
        kwargs['title'] = "Analyze Video"
        wx.Dialog.__init__(self, parent, id,**kwargs)
        
        pvbox = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, wx.ID_ANY)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        label = wx.StaticText(panel,wx.ID_ANY,label="Analyzing a video can take a long time, so be warned!")
        
        self.faceCheck = wx.CheckBox(panel,wx.ID_ANY,label="Find Faces in Video")
        self.faceScaleLabel = wx.StaticText(panel,wx.ID_ANY,label="Scale before finding? (enter None for no or a tuple representing the size to scale to)")
        self.faceScale = wx.TextCtrl(panel, wx.ID_ANY,value="(500,500)")
        self.faceParams = wx.TextCtrl(panel, wx.ID_ANY,value="{'scale_factor':1.1, 'min_neighbors':3, 'flags':0, 'min_size':(10,10)}")
        
        self.trackCheck = wx.CheckBox(panel,wx.ID_ANY,label="Track Faces in Video")
        self.trackParams = wx.TextCtrl(panel, wx.ID_ANY,value="{'look_ahead_threshold':10,'similarity':0.75,'min_track_size':10}")
        
        self.recognizeCheck = wx.CheckBox(panel,wx.ID_ANY,label="recognize Faces in Video")
        self.recognizeParams = wx.TextCtrl(panel, wx.ID_ANY,value="not yet, sorry")
        
        pvbox.Add(label,0,wx.EXPAND)        
        pvbox.Add(self.faceCheck,0,wx.EXPAND)
        pvbox.Add(self.faceScaleLabel,0,wx.EXPAND)
        pvbox.Add(self.faceScale,0,wx.EXPAND)
        pvbox.Add(self.faceParams,0,wx.EXPAND)
        pvbox.Add(self.trackCheck,0,wx.EXPAND)
        pvbox.Add(self.trackParams,0,wx.EXPAND)
        pvbox.Add(self.recognizeCheck,0,wx.EXPAND)
        pvbox.Add(self.recognizeParams,0,wx.EXPAND)
        panel.SetSizer(pvbox)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, wx.ID_OK, "Analyze") 
        hbox.Add(okButton, 1)

        vbox.Add(panel)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        self.SetSizer(vbox)
        vbox.Fit(self)
        
class ShowOverlaysDialog(wx.Dialog):
    def __init__(self, parent, id,bounds,track,recognize,**kwargs):
        kwargs['title'] = "Show Overlays"
        wx.Dialog.__init__(self, parent, id,**kwargs)
        
        pvbox = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, wx.ID_ANY)
        vbox = wx.BoxSizer(wx.VERTICAL)        
        
        comp = []
        if not bounds and not track and not recognize:
            comp.append(wx.StaticText(panel,wx.ID_ANY,label="You need to run some analysis first!"))
        else:
            if bounds:
                self.faceCheck = wx.CheckBox(panel,wx.ID_ANY,label="Show All Faces in Video")
                comp.append(self.faceCheck)
            if track:
                self.trackCheck = wx.CheckBox(panel,wx.ID_ANY,label="Show Tracked Faces in Video")
                comp.append(self.trackCheck)
            if recognize:        
                self.recognizeCheck = wx.CheckBox(panel,wx.ID_ANY,label="Show Recognized Faces in Video")
                comp.append(self.recognizeCheck)
        
        for c in comp:
            pvbox.Add(c,0,wx.EXPAND)
            
        panel.SetSizer(pvbox)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, wx.ID_OK, "Show!")
        hbox.Add(okButton, 1)

        vbox.Add(panel)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        self.SetSizer(vbox)
        vbox.Fit(self)