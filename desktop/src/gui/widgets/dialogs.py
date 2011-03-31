'''
Created on Feb 3, 2011

@author: Alex Levenson (alex@isnotinvain.com)
'''

import wx
import wx.media
import video

class NewStoryDialog(wx.Dialog):
    def __init__(self, parent, id, **kwargs):
        kwargs['title'] = "Create a New Story"
        wx.Dialog.__init__(self, parent, id, **kwargs)

        pvbox = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, wx.ID_ANY)
        vbox = wx.BoxSizer(wx.VERTICAL)

        dirhbox = wx.BoxSizer(wx.HORIZONTAL)

        dirLabel = wx.StaticText(panel, wx.ID_ANY, label="Enter a directory to store Raconteur's data:")
        self.directoryCtrl = wx.TextCtrl(panel, wx.ID_ANY)
        self.directoryCtrl.SetEditable(False)
        def browse(event):
            d = wx.DirDialog(self, message="Select a directory", style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
            if d.ShowModal() == wx.ID_OK:
                self.directoryCtrl.SetValue(d.GetPath())
            d.Destroy()
        self.directoryButton = wx.Button(panel, wx.ID_ANY, label="Browse...")
        self.directoryButton.Bind(wx.EVT_BUTTON, browse)

        nameLabel = wx.StaticText(panel, wx.ID_ANY, label="Enter a name for this story:")
        self.nameCtrl = wx.TextCtrl(panel, wx.ID_ANY)

        dirhbox.Add(self.directoryCtrl, 90, wx.EXPAND)
        dirhbox.Add(self.directoryButton, 10, wx.EXPAND)

        pvbox.Add(dirLabel, 0, wx.EXPAND)
        pvbox.Add(dirhbox, 0, wx.EXPAND)
        pvbox.Add(nameLabel, 0, wx.EXPAND)
        pvbox.Add(self.nameCtrl, 0, wx.EXPAND)
        panel.SetSizer(pvbox)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, wx.ID_OK, "Create!")
        hbox.Add(okButton, 1)

        vbox.Add(panel)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        self.SetSizer(vbox)
        vbox.Fit(self)

class ImportDialog(wx.Dialog):
    def __init__(self, parent, id, **kwargs):
        kwargs['title'] = "Import to this Story"
        wx.Dialog.__init__(self, parent, id, **kwargs)

        pvbox = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, wx.ID_ANY)
        vbox = wx.BoxSizer(wx.VERTICAL)

        dirhbox = wx.BoxSizer(wx.HORIZONTAL)

        dirLabel = wx.StaticText(panel, wx.ID_ANY, label="Enter the path to the file / root of the files you want to import")
        self.directoryCtrl = wx.TextCtrl(panel, wx.ID_ANY)
        self.directoryCtrl.SetEditable(False)
        regexLabel = wx.StaticText(panel, wx.ID_ANY, label="Enter an optional filter regex such as (*.avi)")
        self.regexCtrl = wx.TextCtrl(panel, wx.ID_ANY, value="*")

        def browse(event):
            d = wx.DirDialog(self, message="Select a directory", style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
            if d.ShowModal() == wx.ID_OK:
                self.directoryCtrl.SetValue(d.GetPath())
            d.Destroy()

        self.directoryButton = wx.Button(panel, wx.ID_ANY, label="Browse...")
        self.directoryButton.Bind(wx.EVT_BUTTON, browse)
        streamTypeLabel = wx.StaticText(panel, wx.ID_ANY, label="Enter the stream type \nex:(video, image, location, etc)")
        self.streamTypeCtrl = wx.TextCtrl(panel, wx.ID_ANY)
        self.moveCheck = wx.CheckBox(panel, wx.ID_ANY, label="Move files instead of copy?")

        pvbox.Add(dirLabel, 0, wx.EXPAND)
        dirhbox.Add(self.directoryCtrl, 90, wx.EXPAND)
        dirhbox.Add(self.directoryButton, 10, wx.EXPAND)
        pvbox.Add(dirhbox, 0, wx.EXPAND)
        pvbox.Add(regexLabel, 0, wx.EXPAND)
        pvbox.Add(self.regexCtrl, 0, wx.EXPAND)
        pvbox.Add(streamTypeLabel, 0, wx.EXPAND)
        pvbox.Add(self.streamTypeCtrl, 0, wx.EXPAND)
        pvbox.Add(self.moveCheck, 0, wx.EXPAND)
        panel.SetSizer(pvbox)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, wx.ID_OK, "Import")
        hbox.Add(okButton, 1)

        vbox.Add(panel)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        self.SetSizer(vbox)
        vbox.Fit(self)

class AnalyzeDialog(wx.Dialog):
    def __init__(self, parent, id, **kwargs):
        kwargs['title'] = "Analyze Video"
        wx.Dialog.__init__(self, parent, id, **kwargs)

        pvbox = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, wx.ID_ANY)
        vbox = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(panel, wx.ID_ANY, label="Analyzing a video can take a long time, so be warned!")

        self.faceCheck = wx.CheckBox(panel, wx.ID_ANY, label="Find Faces in Video")
        self.faceScaleLabel = wx.StaticText(panel, wx.ID_ANY, label="Scale before finding? (enter None for no or a tuple representing the size to scale to)")
        self.faceScale = wx.TextCtrl(panel, wx.ID_ANY, value="(500,500)")
        self.faceParams = wx.TextCtrl(panel, wx.ID_ANY, value="{'scale_factor':1.1, 'min_neighbors':3, 'flags':0, 'min_size':(10,10)}")

        self.trackCheck = wx.CheckBox(panel, wx.ID_ANY, label="Track Faces in Video")
        self.trackParams = wx.TextCtrl(panel, wx.ID_ANY, value="{'look_ahead_threshold':10,'similarity':0.60,'min_track_size':30}")

        self.extractCheck = wx.CheckBox(panel, wx.ID_ANY, label="Extract Faces from Video")
        self.extractParams = wx.TextCtrl(panel, wx.ID_ANY, value="{'scaleTo':(200,200)}")

        self.recognizeCheck = wx.CheckBox(panel, wx.ID_ANY, label="Recognize Faces in Video")
        self.recognizeParams = wx.TextCtrl(panel, wx.ID_ANY, value="{}")

        pvbox.Add(label, 0, wx.EXPAND)
        pvbox.Add(self.faceCheck, 0, wx.EXPAND)
        pvbox.Add(self.faceScaleLabel, 0, wx.EXPAND)
        pvbox.Add(self.faceScale, 0, wx.EXPAND)
        pvbox.Add(self.faceParams, 0, wx.EXPAND)
        pvbox.Add(self.trackCheck, 0, wx.EXPAND)
        pvbox.Add(self.trackParams, 0, wx.EXPAND)
        pvbox.Add(self.extractCheck, 0, wx.EXPAND)
        pvbox.Add(self.extractParams, 0, wx.EXPAND)
        pvbox.Add(self.recognizeCheck, 0, wx.EXPAND)
        pvbox.Add(self.recognizeParams, 0, wx.EXPAND)
        panel.SetSizer(pvbox)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, wx.ID_OK, "Analyze")
        hbox.Add(okButton, 1)

        vbox.Add(panel)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        self.SetSizer(vbox)
        vbox.Fit(self)

class ShowOverlaysDialog(wx.Dialog):
    def __init__(self, parent, id, bounds, track, recognize, **kwargs):
        kwargs['title'] = "Show Overlays"
        wx.Dialog.__init__(self, parent, id, **kwargs)

        pvbox = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, wx.ID_ANY)
        vbox = wx.BoxSizer(wx.VERTICAL)

        comp = []
        if not bounds and not track and not recognize:
            comp.append(wx.StaticText(panel, wx.ID_ANY, label="You need to run some analysis first!"))
        else:
            if bounds:
                self.faceCheck = wx.CheckBox(panel, wx.ID_ANY, label="Show All Faces in Video")
                comp.append(self.faceCheck)
            if track:
                self.trackCheck = wx.CheckBox(panel, wx.ID_ANY, label="Show Tracked Faces in Video")
                comp.append(self.trackCheck)
            if recognize:
                self.extractCheck = wx.CheckBox(panel, wx.ID_ANY, label="Show Recognized Faces in Video")
                comp.append(self.extractCheck)

        for c in comp:
            pvbox.Add(c, 0, wx.EXPAND)

        panel.SetSizer(pvbox)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, wx.ID_OK, "Show!")
        hbox.Add(okButton, 1)

        vbox.Add(panel)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        self.SetSizer(vbox)
        vbox.Fit(self)
