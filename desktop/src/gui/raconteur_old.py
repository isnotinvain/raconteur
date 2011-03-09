'''
Created on Feb 2, 2011

@author: Alex Levenson (alex@isnotinvain.com)
'''
import os
import sys
import cPickle
import random
import wx
from widgets import VideoPanel
from stream.importer import StreamImporter 
import util.filesystem
import widgets
import videoOverlays
import vision.finder
import vision.tracker

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
        
        self.loadStory("/home/alex/Documents/raconteur/Test Data/test")
        
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
                                        ("&Reset","Reset the current video"),
                                    )
                    ),
                    ("Analy&ze",   (
                                        ("Show &Faces","Show faces in this video"),
                                        ("Show Face &Tracks","Show face tracks in this video"),
                                        ("&Save Face Tracks","Save the face tracks in this video")
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
        
    def _menuOn_playback_reset(self,event):
        self.currentVideo.reset()
        
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
        self.streamTree.SetPath(self.story)
        self.streamTree.Show()        

    def loadFile(self,event):
        file = self.streamTree.GetFilePath() 
        if file:
            self.videoPanel.loadVideo(file)
            self.currentVideo = self.videoPanel.video
            
    def _menuOn_analyze_showfaces(self,event):
        try:
            self.currentVideo.loadFaceBounds()
        except:
            self.currentVideo.reset()
            finder = vision.finder.ObjectFinder()
            progDialog = wx.ProgressDialog("Extracting Face Boundaries","Working...",maximum=1000,parent=self,style=wx.PD_CAN_ABORT)                        
            self.currentVideo.face_bounds = finder.findInVideo(self.videoPanel.video,progDialog=progDialog)
            self.currentVideo.writeFaceBounds()
            progDialog.Destroy()
            self.videoPanel.video.reset()

        rectSprites = {}
        for frameNo,listOfBounds in enumerate(self.currentVideo.face_bounds):            
            rectSprites[frameNo] = []
            for (x,y,w,h),_ in listOfBounds:
                rectSprites[frameNo].append(videoOverlays.Rect(x,y,w,h))
                
        drawer = videoOverlays.VideoOverlay(rectSprites)               
        self.videoPanel.overlays = [drawer]
        self.videoPanel.play()
    
    def _menuOn_analyze_showfacetracks(self,event):
        try:
            self.currentVideo.loadFaceBounds()
        except:
            d = wx.MessageDialog(self,"You need to run show faces first!","Wooops!",wx.OK)
            d.ShowModal()
            d.Destroy()
            return
                
        try:
            self.currentVideo.loadFaceTracks()
        except:
            tracker = vision.tracker.ObjectTracker()
            #if len(raw_bounds) > 1000:
            #    progDialog = wx.ProgressDialog("Tracking Faces...","Working...",maximum=len(raw_bounds),parent=self,style=wx.PD_CAN_ABORT)
            #    tracks = tracker.extractTracks(raw_bounds,progDialog)
            #    progDialog.Destroy()
            self.currentVideo.face_tracks = tracker.extractAndInerpolateTracks(self.currentVideo.face_bounds)
            self.currentVideo.writeFaceTracks()
            
        colors = {}
        for track in self.currentVideo.face_tracks:
            colors[id(track)] = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
                            
        rectSprites = {}
        for frameNo in xrange(len(self.currentVideo.face_bounds)):
            rectSprites[frameNo] = []
            for track in self.currentVideo.face_tracks:                
                if len(track) < 20: continue
                if frameNo in track:
                    rectSprites[frameNo].append(videoOverlays.Rect(*track[frameNo],color=colors[id(track)]))
                    
        drawer = videoOverlays.VideoOverlay(rectSprites)               
        self.videoPanel.overlays = [drawer]
        self.videoPanel.play()

    def _menuOn_analyze_savefacetracks(self,event):
        try:
            self.currentVideo.loadFaceBounds()
        except:
            d = wx.MessageDialog(self,"You need to run show faces first!","Wooops!",wx.OK)
            d.ShowModal()
            d.Destroy()
            return

        try:
            self.currentVideo.loadFaceTracks()
        except:
            d = wx.MessageDialog(self,"You need to run show face tracks first!","Wooops!",wx.OK)
            d.ShowModal()
            d.Destroy()
            return
                
        self.currentVideo.reset()
        progDialog = wx.ProgressDialog("Working","Working...",maximum=self.currentVideo.getFrameCount(),parent=self,style=wx.PD_CAN_ABORT)
        for frameNo,frame in enumerate(self.currentVideo.frames()):
            for track in self.currentVideo.face_tracks:
                if frameNo in track:
                    path = os.path.join(self.story,"tmp tracks",str(id(track)))
                    util.filesystem.ensureDirectoryExists(path)
                    path = os.path.join(path,str(frameNo)+".jpg")
                    util.image.saveCvSubRect(path,frame, track[frameNo])
                    
                    cont,_ = progDialog.Update(frameNo,"Working...")
                    if not cont:
                        progDialog.Destroy()
                        return
        progDialog.Destroy()        

if __name__ == "__main__":
    app = wx.App(False)
    frame = RaconteurMainWindow(sys.argv[0])
    app.MainLoop()