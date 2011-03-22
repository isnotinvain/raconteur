import wx
import wx.media
import cv
import util.geometry

class VideoScrollPanel(wx.ScrolledWindow):
    
    def __init__(self,parent,orientation,**kwargs):
        wx.ScrolledWindow.__init__(self,parent,**kwargs)
        self.Bind(wx.EVT_SIZE,self.scaleVideos)
        #self.Bind(wx.EVT_PAINT,self.onPaint)
        self.orientation = orientation
        self.SetSizer(wx.BoxSizer(orientation))
        self.loadVideos([])
        self.SetScrollRate(20,20)
        self.zoom = 1.0
    
    def onPaint(self,event):
        dc = wx.AutoBufferedPaintDC(self)
        event.Skip()
                
    def scaleVideos(self,event=None):
        if self.videos:                     
            dependent,zoomable = self.GetClientSize()
            
            if self.orientation != wx.HORIZONTAL:
                dependent,zoomable = zoomable,dependent

            zoom = zoomable * self.zoom

            for video in self.videos:
                w,h = util.geometry.getScaledDimensions(video.GetBestSize(), (dependent,zoom))
                video.SetMinSize((w,h))
                video.SetMaxSize((w,h))
        self.Layout()
        if event: event.Skip()
    
    def loadVideos(self,filePaths):
        self.videos = []
        for path in filePaths:
            
            #HACK to get size of video
            capture = cv.CreateFileCapture(path)
            if not capture or str(capture) == "<Capture (nil)>":
                raise Exception("Couldn't load file: " + path)
            size = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH),cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT)            
            capture = None
            
            video = wx.media.MediaCtrl(self,size=size)
            video.Bind(wx.media.EVT_MEDIA_LOADED, self.scaleVideos)
            video.Load(path)
            self.GetSizer().Add(video,0,wx.EXPAND)
            video.SetMinSize((-1,-1))
            self.videos.append(video)
        self.scaleVideos()
        
class VideoContainer(wx.Panel):
    def __init__(self,parent,orientation,**kwargs):
        wx.Panel.__init__(self,parent)
        
        self.scrollwindow = VideoScrollPanel(self,orientation,**kwargs)       
        box = wx.BoxSizer(orientation)
        
        def onZoom(event):
            self.scrollwindow.zoom = self.zoomControl.GetValue()/1000.0
            self.scrollwindow.scaleVideos()
        
        if orientation == wx.HORIZONTAL:            
            self.zoomControl = wx.Slider(self,wx.ID_ANY,0,0,1000,style=wx.SL_VERTICAL|wx.SL_INVERSE)            
            box.Add(self.zoomControl,0,wx.EXPAND)
            box.Add(self.scrollwindow,1,wx.EXPAND)
        else:
            self.zoomControl = wx.Slider(self,wx.ID_ANY,0,0,1000)            
            box.Add(self.scrollwindow,1,wx.EXPAND)
            box.Add(self.zoomControl,0,wx.EXPAND)
        
        self.zoomControl.Bind(wx.EVT_SLIDER,onZoom)
        
        self.SetSizer(box)
    
    def loadVideos(self,filePaths):
        self.scrollwindow.loadVideos(filePaths)
        
        