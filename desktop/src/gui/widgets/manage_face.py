import os
import wx
import wx.media
import stream.models
import video

class ManageAFacePanel(wx.Panel):

    def __init__(self, parent, video_path, addcallback, delcallback):
        wx.Panel.__init__(self, parent)

        self.vidpanel = video.VideoPanel(self, video_path)
        self.vidpanel.Bind(wx.media.EVT_MEDIA_LOADED, self.onLoad)

        label = wx.StaticText(self, label="Enter this person's name:")
        self.nameCtrl = wx.TextCtrl(self, wx.ID_ANY)

        def add(event):
            addcallback(self.vidpanel.path, self.nameCtrl.GetValue())
            self.vidpanel.Hide()
            self.nameCtrl.Clear()

        addButton = wx.Button(self, label="Add to database")
        addButton.Bind(wx.EVT_BUTTON, add)

        def discard(event):
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
    def __init__(self, parent, person, addcallback, delcallback, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER):
        if person.name == "<unrecognized>":
            title = "Manage Unrecognized Faces"
        else:
            title = "Manage %s's Faces" % person.name
        wx.Frame.__init__(self, parent, title=title, size=(500, 500))

        self.parent = parent
        self.person = person
        self.addcallback = addcallback
        self.delcallback = delcallback

        self.manageAFace = ManageAFacePanel(self, None, addcallback, delcallback)

        def onClick(event):
            vp = event.EventObject
            self.manageAFace.loadFile(vp.path)

        self.onClick = onClick

        self.stack = video.VideoStack(self, wx.VERTICAL, video.PeopleVideoPanel)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        hbox.Add(self.stack, 30, wx.EXPAND)
        hbox.Add(self.manageAFace, 70, wx.EXPAND)

        self.SetSizer(hbox)

        self.crawl()

    def crawl(self):
        self.stack.clear()
        pathsAndManuals = map(lambda x : (x.faces, x.manuallyTagged), self.person.person_appearances)
        self.stack.loadThumbs(pathsAndManuals)
        self.stack.bindAll(self.onClick)
