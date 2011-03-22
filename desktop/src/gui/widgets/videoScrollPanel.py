import wx
import wx.media
import cv
import util.image

class VideoScrollPanel(wx.Panel):
    
    def __init__(self,parent,orientation,**kwargs):            
        wx.Panel.__init__(self,parent,**kwargs)
        self.Bind(wx.EVT_SIZE,self.onSize)
        self.orientation = orientation
        self.loadThumbs([])
        self.zoom = 0.0
        self.scroll = 0.0
                    
    def onSize(self,event):
        self.uiUpdate()
        event.Skip()
        
    def recalc(self):
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
            for vidPanel in self.videos:                
                w,h = vidPanel.size
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
            for i,vidPanel in enumerate(self.videos):
                w,h = vidPanel.size
                factor = factors[i]
                w*=factor
                h*=factor
                vidPanel.SetSize((w,h))
                vidPanel.SetMinSize((w,h))
                vidPanel.SetMaxSize((w,h))
                
                if self.orientation != wx.HORIZONTAL:
                    vidPanel.SetPosition((0,x))
                    x+=h
                else:
                    vidPanel.SetPosition((x,0))
                    x+=w
    
    def uiUpdate(self,event=None):
        self.recalc()
        self.Refresh()
    
    def loadThumbs(self,filePaths):
        self.videos = []
        self.totalWidth = 0
        self.totalHeight = 0
        for path in filePaths:            
            vidPanel = VideoPanel(self,path)
            self.totalWidth += vidPanel.size[0]
            self.totalHeight += vidPanel.size[1]
            self.videos.append(vidPanel)
        self.uiUpdate()

class VideoPanel(wx.Panel):
    def __init__(self,parent,path,**kwargs):            
        wx.Panel.__init__(self,parent,**kwargs)
        self.path = path
        box = wx.BoxSizer(wx.HORIZONTAL)
        
        #HACK to get size of video
        capture = cv.CreateFileCapture(path)
        if not capture or str(capture) == "<Capture (nil)>":
            raise Exception("Couldn't load file: " + path)
        self.size = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH),cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT)
        self.SetMinSize((-1,-1))
        self.thumb = cv.QueryFrame(capture)
        self.thumb = util.image.cvToWx(self.thumb)
        capture = None        
        self.SetSizer(box)
        self.Bind(wx.EVT_PAINT,self.onPaint)
        
    def onPaint(self,event):
        dc = wx.AutoBufferedPaintDC(self)
        w,h = dc.GetSize()
        thumb = self.thumb.Scale(w,h,wx.IMAGE_QUALITY_NORMAL)
        thumb = wx.BitmapFromImage(thumb)
        dc.DrawBitmap(thumb,0,0)
    
    def load(self):
        self.video = wx.media.MediaCtrl(self,size=self.size)
        self.video.Load(self.path)
        self.video.SetMinSize((-1,-1))
        sz = self.GetSizer()
        sz.Clear(True)
        sz.Add(self.video,1,wx.EXPAND)
        
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
    
    def loadThumbs(self,filePaths):
        self.scrollwindow.loadThumbs(filePaths)
        