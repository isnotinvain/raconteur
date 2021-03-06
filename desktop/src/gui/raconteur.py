'''
Raconteur (c) Alex Levenson 2011
All rights reserved

@author: Alex Levenson (alex@isnotinvain.com)

Main UI Entrance point
This is the script you run to boot up Raconteur
'''
import sys
import wx
import widgets
import widgets.video
import uifunctions
import stream.story
import stream.models
import util.filesystem

class RaconteurMainWindow(wx.Frame):
    """
    Raconteur's main UI window
    @author: Alex Levenson (alex@isnotinvain.com)
    """

    ABOUT = """
            Raconteur
            A Senior Design Project by Alex Levenson
            (alex@isnotinvain.com)
            Raconteur performs face tracking and face recognition
            in video files. Raconteur hopes to become a blogging
            utility that helps you write your video blog.
            """

    def __init__(self, storyPath):
        wx.Frame.__init__(self, None, title="Raconteur\t|\tYour Life is a Story", size=(800, 700))
        self.story = None
        self.__setupLayoutAndWidgets()

        def quit(evt):
            evt.Skip()

        self.Bind(wx.EVT_CLOSE, quit)
        self.loadStory(storyPath)
        self.currentVideo = None
        self.Show(True)

    def loadStory(self, path):
        if not path: return
        try:
            self.story = stream.story.Story.load(path)
        except:
            self.story = None
            widgets.messageBox(self, "Couldn't load story from: " + path, "Error loading story")
            return
        util.filesystem.ensureDirectoryExists(self.story.getPeopleDir())
        util.filesystem.ensureDirectoryExists(self.story.getUnrecognizedPeopleDir())
        self.SetTitle(self.story.name)
        #self.story.clearDb()
        self.story.recrawl("video", stream.models.Video)
        self.reloadTimeline()
        self.reloadPeoplePanel()

    def reloadTimeline(self):
        paths = []
        for vid in stream.models.Video.query.order_by('creation').all():
            paths.append(vid.path)

        self.timeline.loadThumbs(paths)

    def reloadPeoplePanel(self):
        paths = []
        for person in stream.models.Person.query.all():
            if person == self.story.getUnrecognizedPerson(): continue
            app = stream.models.PersonAppearance.get_by(person=person)
            if app:
                vid = app.faces
                paths.append(vid)

        self.peoplePanel.loadThumbs(paths)

    def __setupLayoutAndWidgets(self):
        self.CreateStatusBar()

        menu_bar = wx.MenuBar()
        for menu, items in uifunctions.menu:
            wxmenu = wx.Menu()
            for i in items:
                if len(i) == 3:
                    item, caption, callback = i
                    id = wx.ID_ANY
                elif len(i) == 4:
                    item, caption, callback, id = i
                else:
                    raise Exception("Bad menu item: " + str(i))

                wxItem = wxmenu.Append(id, item, caption)
                prefix = "_menu_on_" + menu.lower().replace("&", "").replace(" ", "")
                setattr(self.__class__, prefix + str(id), callback)
                self.Bind(wx.EVT_MENU, getattr(self, prefix + str(id)), wxItem)
            menu_bar.Append(wxmenu, menu)
        self.SetMenuBar(menu_bar)

        self.toolbar = wx.ToolBar(self, wx.ID_ANY, style=wx.TB_VERTICAL)
        for tool, callback in uifunctions.tools:
            id = wx.NewId()
            button = wx.Button(self.toolbar, id, tool)
            setattr(self.__class__, "_toolbar_on_" + str(id), callback)
            button.Bind(wx.EVT_BUTTON, getattr(self, "_toolbar_on_" + str(id)), button)
            self.toolbar.AddControl(button)
        self.toolbar.Realize()

        for func, name in uifunctions.extra:
            setattr(self.__class__, name, func)

        self.videoPanel = widgets.video.VideoPanel(self)
        self.videoPanel.enableOverlays()
        self.peoplePanel = widgets.video.VideoStack(self, wx.VERTICAL)
        self.timeline = widgets.video.VideoStack(self, wx.HORIZONTAL)

        self.timeline.Bind(widgets.video.ClickToPlayVideoPanel.EVT_LOAD_VIDEO, self.loadVideo)
        self.peoplePanel.Bind(widgets.video.ClickToPlayVideoPanel.EVT_LOAD_VIDEO, self.onManagePerson)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.toolbar, 0, wx.EXPAND)
        hsizer.SetItemMinSize(0, self.toolbar.GetMinSize())
        hsizer.Add(self.videoPanel, 80, wx.EXPAND)
        hsizer.Add(self.peoplePanel, 20, wx.EXPAND)

        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(hsizer, 80, wx.EXPAND)

        vsizer.Add(self.timeline, 20, wx.EXPAND)

        self.SetSizer(vsizer)
        self.SetAutoLayout(True)

    def loadVideo(self, event):
        self.videoPanel.load(event.path)
        self.currentVideo = event.path
        self.Layout()

if __name__ == "__main__":
    # Boot up Raconteur!
    app = wx.App(False)
    if len(sys.argv) == 2:
        frame = RaconteurMainWindow(sys.argv[1])
    else:
        frame = RaconteurMainWindow(None)
    app.MainLoop()
