import wx
import wx.media
import cv

class VideoScrollPanel(wx.ScrolledWindow):
    
    def __init__(self,parent,orientation,**kwargs):        
        
        if orientation == wx.HORIZONTAL:
            kwargs["style"] = wx.HSCROLL
        else:
            kwargs["style"] = wx.VSCROLL
            
        wx.ScrolledWindow.__init__(self,parent,**kwargs)
        self.Bind(wx.EVT_SIZE,self.onSize)
        
        self.brush = wx.TRANSPARENT_BRUSH
        self.pen = wx.Pen((100,100,100),2)
        
        self.orientation = orientation
        self.SetSizer(wx.BoxSizer(orientation))
        self.loadVideos([])
        self.zoom = 0.0
        self.z = 0
                    
    def onSize(self,event):
        print self.z
        self.z+=1
    
    def scaleVideos(self):
        if self.videos:
            width,height = self.GetClientSize()
            
            if self.orientation != wx.HORIZONTAL:
                width,height = height,width
                totalWidth = self.totalHeight
            else:
                totalWidth = self.totalWidth            
            
            minFactor = width / float(totalWidth)            
            for video in self.videos:
                w,h = video.GetBestSize()                    
                if w == 0 or h == 0 : return
                if self.orientation != wx.HORIZONTAL:
                    maxFactor = float(height) / w
                else:
                    maxFactor = float(height) / h
                                        
                factor = minFactor + (maxFactor-minFactor)*self.zoom
                w*=factor
                h*=factor
                
                video.SetMinSize((w,h))
                video.SetMaxSize((w,h))
    
    def uiUpdate(self,event=None):
        self.scaleVideos()
        self.Layout()
        self.FitInside()
        self.SetScrollRate(20,20)
    
    def loadVideos(self,filePaths):
        self.videos = []
        self.totalWidth = 0
        self.totalHeight = 0
        for path in filePaths:
            
            #HACK to get size of video
            capture = cv.CreateFileCapture(path)
            if not capture or str(capture) == "<Capture (nil)>":
                raise Exception("Couldn't load file: " + path)
            size = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH),cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT)            
            capture = None
            
            self.totalWidth += size[0]
            self.totalHeight += size[1]
            
            video = wx.media.MediaCtrl(self,size=size)
            video.Bind(wx.media.EVT_MEDIA_LOADED, self.uiUpdate)
            video.Load(path)
            self.GetSizer().Add(video,0,wx.EXPAND)
            video.SetMinSize((-1,-1))
            self.videos.append(video)
        self.uiUpdate()
        
class VideoContainer(wx.Panel):
    def __init__(self,parent,orientation,**kwargs):
        wx.Panel.__init__(self,parent)
        
        self.scrollwindow = VideoScrollPanel(self,orientation,**kwargs)       
        box = wx.BoxSizer(orientation)
        
        def onZoom(event):
            self.scrollwindow.zoom = self.zoomControl.GetValue()/1000.0
            self.scrollwindow.uiUpdate()
        
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
        