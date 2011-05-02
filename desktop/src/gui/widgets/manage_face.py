'''
Raconteur (c) Alex Levenson 2011
All rights reserved

@author: Alex Levenson (alex@isnotinvain.com)

Widgets involved with managing the faces database
'''

import os
import wx
import wx.media
import stream.models
import video

class ManageAFacePanel(wx.Panel):
    """
    A Panel for managing a single face
    """
    def __init__(self, parent, video_path, addcallback, delcallback):
        wx.Panel.__init__(self, parent)

        self.vidpanel = video.VideoPanel(self, video_path)
        self.vidpanel.Bind(wx.media.EVT_MEDIA_LOADED, self.onLoad)

        label = wx.StaticText(self, label="Enter this person's name:")
        self.nameCtrl = wx.TextCtrl(self, wx.ID_ANY)

        def add(event):
            """
            Called when a face is added to the database
            """
            addcallback(self.vidpanel.path, self.nameCtrl.GetValue())
            self.vidpanel.Hide()
            self.nameCtrl.Clear()

        addButton = wx.Button(self, label="Add to database")
        addButton.Bind(wx.EVT_BUTTON, add)

        def discard(event):
            """
            Called when a face is discarded
            """
            delcallback(self.vidpanel.path)
            self.vidpanel.Hide()
            self.nameCtrl.Clear()

        discardButton = wx.Button(self, label="Discard this face")
        discardButton.Bind(wx.EVT_BUTTON, discard)

        vStack = wx.BoxSizer(wx.VERTICAL)

        vidbox = wx.BoxSizer(wx.HORIZONTAL)
        vidbox.AddStretchSpacer(1)
        vidbox.Add(self.vidpanel, 0, wx.SHAPED)
        vidbox.AddStretchSpacer(1)

        vStack.AddStretchSpacer(1)
        vStack.Add(vidbox, 0, wx.EXPAND)
        vStack.AddStretchSpacer(1)
        vStack.Add(label, 0, wx.EXPAND)
        vStack.Add(self.nameCtrl, 0, wx.EXPAND)
        buttonsBox = wx.BoxSizer(wx.HORIZONTAL)
        buttonsBox.Add(discardButton, 1, wx.EXPAND)
        buttonsBox.Add(addButton, 1, wx.EXPAND)
        vStack.Add(buttonsBox, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM)
        self.SetSizer(vStack)

    def onLoad(self, event):
        self.vidpanel.SetMinSize((200, 200))
        self.Layout()
        self.Refresh()
        self.vidpanel.play()
        self.vidpanel.Show()

    def loadFile(self, path):
        self.vidpanel.load(path)
        self.vidpanel.load()

    def clear(self):
        self.vidpanel.clear()


class ManageFaces(wx.Frame):
    """
    The dialog for managing all of a single person's faces
    """
    def __init__(self, parent, person, addcallback, delcallback, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER):
        if person.name == "<unrecognized>":
            title = "Manage Unrecognized Faces"
        else:
            title = "Manage %s's Faces" % person.name
        wx.Frame.__init__(self, parent, title=title, size=(700, 500))

        self.parent = parent
        self.person = person
        self.addcallback = addcallback
        self.delcallback = delcallback

        self.manageAFace = ManageAFacePanel(self, None, addcallback, delcallback)

        def onClick(event):
            vp = event.EventObject
            self.manageAFace.loadFile(vp.path)

        def onTimelineClick(event):
            self.parent.loadVideo(event)

        self.onClick = onClick

        self.stack = video.VideoStack(self, wx.VERTICAL, video.PeopleVideoPanel)
        self.timeline = video.VideoStack(self, wx.VERTICAL)
        self.Bind(video.ClickToPlayVideoPanel.EVT_LOAD_VIDEO, onTimelineClick)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        hbox.Add(self.stack, 30, wx.EXPAND)
        hbox.Add(self.manageAFace, 40, wx.EXPAND)
        hbox.Add(self.timeline, 30, wx.EXPAND)

        self.SetSizer(hbox)

        self.crawl()

    def crawl(self):
        self.stack.clear()
        pathsAndManuals = map(lambda x : (x.faces, x.manuallyTagged), self.person.person_appearances)
        pathsAndManuals = [x for x in pathsAndManuals if x[0]]
        self.stack.loadThumbs(pathsAndManuals)
        self.stack.bindAll(self.onClick)

        self.timeline.clear()
        appearances = set(map(lambda x : str(x.path), self.person.appearsIn))
        self.timeline.loadThumbs(appearances)
