import sys
import wx
import widgets
import uistructure
import stream.story

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
    
    def __init__(self,storyPath):        
        wx.Frame.__init__(self, None,title="Raconteur\t|\tYour Life is a Story",size=(1500,800))        
        self.story = None
        self.__setupLayoutAndWidgets()
        
        def quit(evt):
            self.videoPanel.pause()
            evt.Skip()        
        self.Bind(wx.EVT_CLOSE,quit)
        
        self.Show(True)        
        self.loadStory(storyPath)
        self.currentVideo = None

    def loadStory(self,path):
        if not path: return
        try:
            self.story = stream.story.Story.load(path)            
        except:
            self.story = None
            widgets.messageBox(self,"Couldn't load story from: "+path,"Error loading story")
            return
        
        self.story.crawl("video")
        self.SetTitle(self.story.name)
        self.timelinePanel.loadThumbs()
            
    def __setupLayoutAndWidgets(self):
        self.CreateStatusBar()
        
        menu_bar = wx.MenuBar()
        for menu,items in uistructure.menu:            
            wxmenu = wx.Menu()            
            for i in items:
                if len(i) == 3:
                    item,caption,callback = i
                    id = wx.ID_ANY
                elif len(i) == 4:
                    item,caption,callback,id = i
                else:
                    raise Exception("Bad menu item: "+str(i))
                
                wxItem = wxmenu.Append(id,item,caption)
                prefix = "_menu_on_"+menu.lower().replace("&","").replace(" ","")
                setattr(self.__class__,prefix+str(id),callback)
                self.Bind(wx.EVT_MENU,getattr(self,prefix+str(id)),wxItem)
            menu_bar.Append(wxmenu,menu)
        self.SetMenuBar(menu_bar)
        
        self.toolbar = wx.ToolBar(self,wx.ID_ANY,style=wx.TB_VERTICAL)
        for tool,callback in uistructure.tools:
            id = wx.NewId()
            button = wx.Button(self.toolbar, id, tool)
            setattr(self.__class__,"_toolbar_on_"+str(id),callback)
            button.Bind(wx.EVT_BUTTON,getattr(self,"_toolbar_on_"+str(id)),button)
            self.toolbar.AddControl(button)
        self.toolbar.Realize()
                
        self.videoPanel = widgets.VideoPanel(self,wx.ID_ANY)
        #self.peoplePanel = widgets.PeoplePanel(self,wx.ID_ANY)        
        self.timelinePanel = widgets.TimelinePanel(self,wx.ID_ANY)
        self.timelineZoomer = wx.Slider(self,wx.ID_ANY,0,0,1000,style=wx.SL_VERTICAL|wx.SL_INVERSE)
        def onZoom(event):
            self.timelinePanel.setZoom(self.timelineZoomer.GetValue()/1000.0)
            self.timelinePanel.Refresh()
        self.timelineZoomer.Bind(wx.EVT_SCROLL,onZoom)
        
        self.timelineScroller = wx.Slider(self,wx.ID_ANY,0,0,1000)
        def onScroll(event):
            self.timelinePanel.setPos(self.timelineScroller.GetValue()/1000.0)
            self.timelinePanel.Refresh()
        self.timelineScroller.Bind(wx.EVT_SCROLL,onScroll)


        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.toolbar,0,wx.EXPAND)
        hsizer.SetItemMinSize(0,self.toolbar.GetMinSize())
        hsizer.Add(self.videoPanel,90,wx.EXPAND)
        #hsizer.Add(self.peoplePanel,10,wx.EXPAND)
        
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(hsizer,80,wx.EXPAND)
        
        hhsizer = wx.BoxSizer(wx.HORIZONTAL)
        hhsizer.Add(self.timelineZoomer,0,wx.EXPAND)
        hhsizer.SetItemMinSize(0,self.timelineZoomer.GetMinSize())               
        hhsizer.Add(self.timelinePanel,100,wx.EXPAND)
        
        vsizer.Add(hhsizer,20,wx.EXPAND)
        vsizer.Add(self.timelineScroller,0,wx.EXPAND)
        vsizer.SetItemMinSize(2,self.timelineScroller.GetMinSize())
        
        self.SetSizer(vsizer)
        self.SetAutoLayout(True)

    def loadVideo(self,path):
        self.videoPanel.loadVideo(path)
        self.Refresh()
        self.Update()
        self.currentVideo = self.videoPanel.video

if __name__ == "__main__":
    app = wx.App(False)
    if len(sys.argv) == 2:
        frame = RaconteurMainWindow(sys.argv[1])
    else:
        frame = RaconteurMainWindow(None)
    app.MainLoop()