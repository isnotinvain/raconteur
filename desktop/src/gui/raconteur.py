'''
Created on Feb 2, 2011

@author: Alex Levenson (alex@isnotinvain.com)
'''
import os
import sys
import cPickle
import wx
from videoPanel import VideoPanel
from stream.video import Video
from stream.importer import StreamImporter 
import util.filesystem
import widgets
from vision.tracker import ObjectTracker
from progressTracker import ProgressTracker
from videoOverlays import VideoOverlay

class RaconteurMainWindow(wx.Frame):
    '''
    The main GUI class for Raconteur
    '''
    ABOUT = """
    Raconteur
    A Senior Design Project by Alex Levenson
    (alex@isnotinvain.com)
    Raconteur performs face tracking and face recognition 
    in video files. Raconteur hopes to become a blogging 
    utility that helps you write your video blog.
    """    
    def __init__(self,script_path):
        wx.Frame.__init__(self, None,title="Raconteur\t|\tYour Life is a Story",size=(800,500))
        self.story = None
        
        self.CreateStatusBar()
        
        self.__setupMenu()
        
        self.__setupLayout()
        
        self.Show(True)
        
        self.loadStory("/home/alex/Desktop/test")
        
        self.currentVideo = None
        
        self.resourcesPath = os.path.join(script_path,"..","resources")
    
    def __setupLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        split = wx.SplitterWindow(self,wx.ID_ANY,style=wx.SP_LIVE_UPDATE)
        self.split = split
        
        sizer.Add(split,1,wx.EXPAND)
        
        self.streamTree = wx.GenericDirCtrl(split,wx.ID_ANY) 
        self.streamTree.Bind(wx.EVT_TREE_SEL_CHANGED, self.loadFile)       
        panel = VideoPanel(split,wx.ID_ANY)
        split.SplitVertically(self.streamTree,panel)        
        
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.FitInside(self)
        split.SetSashPosition(300,True)
        self.videoPanel = panel
        self.streamTree.Hide()
        
    def __setupMenu(self):
        '''
        Sets up the menu bar at the top of the windo
        '''
        MENU =  (
                    ("&File",    (
                                    ("&New Story","Create a new story"),
                                    ("&Open Story","Open a new story"),
                                    ("E&xit","Close Raconteur",wx.ID_EXIT),
                                )
                    ),
                    
                    ("&Playback",   (
                                        ("Pla&y","Play the current video"),
                                        ("Pau&se","Pause the current video"),
                                    )
                    ),
                    ("Analy&ze",   (
                                        ("Show &Faces","Show faces in this video"),
                                        ("Show Face &Tracks","Show face tracks in this video"),
                                    )
                    ),
                    ("&Import",  (
                                    ("Fi&le","Import a single file"),
                                    ("&Directory","Import a directory"),
                                )
                    ),                    
                    ("&Help",    (
                                    ("&About","About Raconteur",wx.ID_ABOUT),
                                )
                    ),
                )

        menu_bar = wx.MenuBar()
        for menu,items in MENU:            
            wxmenu = wx.Menu()            
            for i in items:
                if len(i) == 2:
                    item,caption = i
                    id = wx.ID_ANY
                else:
                    item,caption,id = i
                wxItem = wxmenu.Append(id,item,caption)
                callback = "_menuOn_"+menu.lower().replace("&","").replace(" ","")+"_"+item.lower().replace("&","").replace(" ","")
                #if hasattr(self,callback):
                callback = getattr(self,callback)
                self.Bind(wx.EVT_MENU,callback,wxItem)
            menu_bar.Append(wxmenu,menu)
        self.SetMenuBar(menu_bar)
    
    def _menuOn_file_exit(self,event):
        self.videoPanel.pause()
        self.Close(True)
    
    def _menuOn_import_file(self,event):
        if not self.story:
            d = wx.MessageDialog(self,"You need to open a story first!","Wooops!",wx.OK)
            d.ShowModal()
            d.Destroy()
        else:
            d = widgets.ImportDialog(self,wx.ID_ANY)
            if d.ShowModal()==wx.ID_OK:
                imp = StreamImporter(d.streamTypeCtrl.GetValue(),self.story,d.moveCheck.GetValue())
                imp.importFile(d.directoryCtrl.GetValue())
                s = wx.MessageDialog(self,"File Imported","Done!",wx.OK)
                s.ShowModal()
                s.Destroy()
            d.Destroy()
    
    def _menuOn_import_directory(self,event):
        if not self.story:
            d = wx.MessageDialog(self,"You need to open a story first!","Wooops!",wx.OK)
            d.ShowModal()
            d.Destroy()
        else:
            d = widgets.ImportDialog(self,wx.ID_ANY)
            if d.ShowModal()==wx.ID_OK:
                imp = StreamImporter(d.streamTypeCtrl.GetValue(),self.story,d.moveCheck.GetValue())
                imp.importDirectory(d.directoryCtrl.GetValue())
                s = wx.MessageDialog(self,"File Imported","Done!",wx.OK)
                s.ShowModal()
                s.Destroy()
            d.Destroy()
    
    def _menuOn_help_about(self,event):
        d = wx.MessageDialog(self, self.ABOUT, "About Raconteur", wx.OK)
        d.ShowModal()
        d.Destroy()

    def _menuOn_playback_pause(self,event):
        self.videoPanel.pause()
        
    def _menuOn_playback_play(self,event):
        self.videoPanel.play()
        
    def _menuOn_file_newstory(self,event):
        d = widgets.NewStoryDialog(self,wx.ID_ANY)
        if d.ShowModal()==wx.ID_OK:
            path = d.directoryCtrl.GetValue()
            name = d.nameCtrl.GetValue()
            util.filesystem.setupNewStoryDirectory(path,name)            
        d.Destroy()
    
    def _menuOn_file_openstory(self,event):
        d = widgets.OpenStoryDialog(self,wx.ID_ANY)
        if d.ShowModal()==wx.ID_OK:
            self.loadStory(d.directoryCtrl.GetValue())
        d.Destroy()
    
    def loadStory(self,story):
        self.story = story
        f = open(os.path.join(self.story,".raconteur"),"r")
        self.storyData = cPickle.load(f)
        f.close()
        #self.streamTree.SetDefaultPath(self.story)
        self.streamTree.SetPath(self.story)
        self.streamTree.Show()        

    def loadFile(self,event):
        file = self.streamTree.GetFilePath() 
        if file:
            self.videoPanel.loadVideo(file)
            self.currentVideo = self.videoPanel.video
            
    def _menuOn_analyze_showfaces(self,event):
        if os.path.exists(self.currentVideo.file_path+".raw_face_bounds.pickle"):
            f = open(self.currentVideo.file_path+".raw_face_bounds.pickle","r")
            raw_bounds = cPickle.load(f)
            f.close()
        else:
            self.videoPanel.video.reset()
            tracker = ObjectTracker(self.videoPanel.video)
            progDialog = wx.ProgressDialog("Working...","Working...",maximum=1000,parent=self,style=wx.PD_CAN_ABORT)            
            tracker.progDialog = progDialog
            tracker.extractRawObjectBounds()
            progDialog.Destroy()
            f = open(self.currentVideo.file_path+".raw_face_bounds.pickle","w")
            cPickle.dump(tracker.raw_bounds,f)
            raw_bounds = tracker.raw_bounds
            self.videoPanel.video.reset()
        
        
        rectSprites = {}
        for frame,n in enumerate(raw_bounds):
            bounds = []
            for 
            
        drawer = VideoOverlay(rectSprites)       
        class BoundDrawer:
            def __init__(self,bounds):
                self.bounds = bounds            
            def draw(self,dc,frameNum):
                frameNum = int(frameNum)
                factor = None
                if hasattr(dc,"ZraconteurScaleFactor"):
                    factor = dc.raconteurScaleFactor
                                    
                if frameNum < len(self.bounds):
                    bound = self.bounds[frameNum]
                    if factor:
                        x = b[0][0] * factor
                        y = b[0][1] * factor
                        w = b[0][2] * factor
                        h = b[0][3] * factor
                        n = b[1]
                        b = ((x,y,w,h),n)
                    util.image.wxDrawObjecBoundaries(dc, bound)
        bd = BoundDrawer(raw_bounds)        
        self.videoPanel.overlays = [bd.draw]
    
    def _menuOn_analyze_showfacetracks(self,event):
        pass

if __name__ == "__main__":
    app = wx.App(False)
    frame = RaconteurMainWindow(sys.argv[0])
    app.MainLoop()