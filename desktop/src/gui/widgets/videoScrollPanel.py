import wx
import wx.media
import cv

class VideoScrollPanel(wx.Panel):
    
    def __init__(self,parent,orientation,**kwargs):            
        wx.Panel.__init__(self,parent,**kwargs)
        self.Bind(wx.EVT_SIZE,self.onSize)
        
        self.brush = wx.TRANSPARENT_BRUSH
        self.pen = wx.Pen((100,100,100),2)
        
        self.orientation = orientation
        self.loadVideos([])
        self.zoom = 0.0
        self.scroll = 0.0
                    
    def onSize(self,event):
        self.uiUpdate()
        event.Skip()
        
    def scaleVideos(self):
        if self.videos:
            width,height = self.GetClientSize()
            
            if self.orientation != wx.HORIZONTAL:
                width,height = height,width
                totalWidth = self.totalHeight
            else:
                totalWidth = self.totalWidth            
            
            minFactor = width / float(totalWidth)
            factors = []
            xTotal = 0
            for video in self.videos:
                w,h = video.GetBestSize()
                if w == 0 or h == 0 : return
                if self.orientation != wx.HORIZONTAL:
                    maxFactor = float(height) / w
                    xInc = h
                else:
                    maxFactor = float(height) / h
                    xInc = w
                
                factor = minFactor + (maxFactor-minFactor)*self.zoom
                factors.append(factor)
                xTotal += factor*xInc

            xDelta = xTotal - width
            if xDelta < 0: xDelta = 0
            x = xDelta*self.scroll*-1
            for i,video in enumerate(self.videos):
                w,h = video.GetBestSize()
                factor = factors[i]
                w*=factor
                h*=factor
                video.SetSize((w,h))
                video.SetMinSize((w,h))
                video.SetMaxSize((w,h))
                
                if self.orientation != wx.HORIZONTAL:
                    video.SetPosition((0,x))
                    x+=h
                else:
                    video.SetPosition((x,0))
                    x+=w
    
    def uiUpdate(self,event=None):
        self.scaleVideos()
    
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
            self.videos.append(video)
        self.uiUpdate()
        
class VideoContainer(wx.Panel):
    def __init__(self,parent,orientation,**kwargs):
        wx.Panel.__init__(self,parent)
        
        self.scrollwindow = VideoScrollPanel(self,orientation,**kwargs)       
        obox = wx.BoxSizer(orientation)
                
        def onZoom(event):
            self.scrollwindow.zoom = self.zoomControl.GetValue()/1000.0
            self.scrollwindow.uiUpdate()
        
        def onScroll(event):
            self.scrollwindow.scroll = self.scrollControl.GetValue()/1000.0
            self.scrollwindow.uiUpdate()
            
        if orientation == wx.HORIZONTAL:            
            self.zoomControl = wx.Slider(self,wx.ID_ANY,0,0,1000,style=wx.SL_VERTICAL|wx.SL_INVERSE)            
            self.scrollControl = wx.Slider(self,wx.ID_ANY,0,0,1000)
            obox.Add(self.zoomControl,0,wx.EXPAND)
            obox.Add(self.scrollwindow,1,wx.EXPAND)
            opBox = wx.BoxSizer(wx.VERTICAL)
            opBox.Add(obox,1,wx.EXPAND)
            opBox.Add(self.scrollControl,0,wx.EXPAND)
        else:
            self.zoomControl = wx.Slider(self,wx.ID_ANY,0,0,1000)
            self.scrollControl = wx.Slider(self,wx.ID_ANY,0,0,1000,style=wx.SL_VERTICAL|wx.SL_INVERSE)
            obox.Add(self.scrollwindow,1,wx.EXPAND)
            obox.Add(self.zoomControl,0,wx.EXPAND)
            opBox = wx.BoxSizer(wx.HORIZONTAL)
            opBox.Add(obox,1,wx.EXPAND)
            opBox.Add(self.scrollControl,0,wx.EXPAND)
            
        self.zoomControl.Bind(wx.EVT_SLIDER,onZoom)
        self.scrollControl.Bind(wx.EVT_SLIDER,onScroll)
        
        self.SetSizer(opBox)
    
    def loadVideos(self,filePaths):
        self.scrollwindow.loadVideos(filePaths)
        