'''
Raconteur (c) Alex Levenson 2011
All rights reserved

@author: Alex Levenson (alex@isnotinvain.com)

Widgets pertaining to videos
'''

import wx
import wx.media
import wx.lib.newevent
import cv
import util.image

class VideoPanel(wx.Panel):
    """
    A simple panel that contains a playable video
    """
    def __init__(self, parent, path=None, **kwargs):
        wx.Panel.__init__(self, parent, **kwargs)
        self.path = path
        box = wx.BoxSizer(wx.HORIZONTAL)
        if not hasattr(self, "videoPen"):
            self.videoPen = wx.TRANSPARENT_PEN
        if not hasattr(self, "videoBrush"):
            self.videoBrush = wx.TRANSPARENT_BRUSH
        self.video = None
        self.thumb = None
        self.overlays = []

        if path: self.loadThumb()

        self.SetSizer(box)

        self.Bind(wx.EVT_PAINT, self.onPaint)

    def enableOverlays(self):
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onOverlay)
        self.timer.Start(10)

    def disableOverlays(self):
        self.timer.Stop()
        self.timer = None

    def onOverlay(self, event):
        if self.video:
            dc = wx.WindowDC(self.video)
            for overlay in self.overlays:
                sec = self.video.Tell()
                sec /= 1000.0
                frameno = sec * self.framerate
                frameno = int(frameno - self.framerate)
                factors = (float(self.video.GetSize()[0]) / self.size[0], float(self.video.GetSize()[1]) / self.size[1])
                overlay.drawFrame(dc, factors, frameno)

    def onPaint(self, event):
        if not self.thumb: return
        dc = wx.AutoBufferedPaintDC(self)
        w, h = dc.GetSize()
        thumb = self.thumb.Scale(w, h, wx.IMAGE_QUALITY_NORMAL)
        thumb = wx.BitmapFromImage(thumb)
        dc.DrawBitmap(thumb, 0, 0)
        dc.SetBrush(self.videoBrush)
        dc.SetPen(self.videoPen)
        dc.DrawRectangle(0, 0, w, h)

    def loadThumb(self, path=None):
        if not path: path = self.path
        if not path: return
        #HACK to get size of video and framerate
        capture = cv.CreateFileCapture(path)
        if not capture or str(capture) == "<Capture (nil)>":
            raise Exception("Couldn't load file: " + path)
        self.size = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH), cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT)
        self.SetInitialSize(self.size)
        self.framerate = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FPS)
        self.SetMinSize((-1, -1))

        self.thumb = cv.QueryFrame(capture)
        self.thumb = util.image.cvToWx(self.thumb)
        capture = None

    def load(self, path=None):
        if not path: path = self.path
        if not path: return
        self.path = path
        self.loadThumb()

        self.video = wx.media.MediaCtrl(self, size=self.size)
        self.video.Load(self.path)
        self.video.SetMinSize((-1, -1))
        sz = self.GetSizer()
        sz.Clear(True)
        sz.Add(self.video, 1, wx.EXPAND)

    def play(self, event=None):
        if self.video:
            self.video.Play()

    def playPause(self, event=None):
        if self.video:
            if self.video.GetState() == wx.media.MEDIASTATE_PLAYING:
                self.pause()
            else:
                self.play()

    def pause(self, event=None):
        if self.video:
            self.video.Pause()

    def stop(self, event=None):
        if self.video:
            self.video.Stop()

    def clear(self):
        self.GetSizer().Clear(True)
        self.ClearBackground()

class ClickToPlayVideoPanel(VideoPanel):
    """
    Overrides some of VideoPanel's methods to change
    how it handles events
    """
    LoadVideoEvent, EVT_LOAD_VIDEO = wx.lib.newevent.NewCommandEvent()

    def __init__(self, parent, path=None, **kwargs):
        VideoPanel.__init__(self, parent, path, **kwargs)
        self.Bind(wx.EVT_LEFT_UP, self.onClick)
        self.Bind(wx.EVT_RIGHT_UP, self.onRClick)
        self.videoPen = wx.Pen((100, 100, 100), 4)
        self.videoBrush = wx.TRANSPARENT_BRUSH

    def load(self, path=None):
        VideoPanel.load(self, path)
        self.video.Bind(wx.EVT_LEFT_UP, self.onVClick)
        self.video.Bind(wx.EVT_RIGHT_UP, self.onRClick)

    def onRClick(self, event):
        evt = self.LoadVideoEvent(self.GetId(), path=self.path)
        evt.EventObject = self
        wx.PostEvent(self.GetParent(), evt)

    def onClick(self, event):
        self.load()
        self.play()
        self.Layout()

    def onVClick(self, event):
        self.stop()
        self.GetSizer().Clear(True)
        self.video = None

class PeopleVideoPanel(VideoPanel):
    """
    The vertical stack of people in the database
    """
    LoadVideoEvent, EVT_LOAD_VIDEO = wx.lib.newevent.NewCommandEvent()

    def __init__(self, parent, path=None, **kwargs):
        if isinstance(path, tuple):
            path, manual = path
            self.manual = manual
            if self.manual:
                self.setColor((0, 0, 255))
            else:
                self.setColor((0, 255, 0))
        VideoPanel.__init__(self, parent, path, **kwargs)
        self.Bind(wx.EVT_LEFT_UP, self.onClick)
        self.videoBrush = wx.TRANSPARENT_BRUSH

    def setColor(self, color):
        self.videoPen = wx.Pen(color, 4)

    def load(self, path=None):
        print "load"
        if isinstance(path, tuple):
            path, manual = path
            self.manual = manual
            if self.manual:
                self.setColor((100, 100, 100))
            else:
                self.setColor((100, 255, 100))

        VideoPanel.load(self, path)

    def onClick(self, event):
        evt = self.LoadVideoEvent(self.GetId(), path=self.path)
        evt.EventObject = self
        wx.PostEvent(self.GetParent(), evt)

class VideoScrollPanel(wx.Panel):
    """
    Helper for the VideoStack
    """
    def __init__(self, parent, orientation, vidPanelType=None, **kwargs):
        wx.Panel.__init__(self, parent, **kwargs)
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.orientation = orientation
        self.loadThumbs([])
        self.zoom = 0.0
        self.scroll = 0.0
        if vidPanelType:
            self.vidPanelType = vidPanelType
        else:
            self.vidPanelType = ClickToPlayVideoPanel

    def onSize(self, event):
        self.uiUpdate()
        event.Skip()

    def recalc(self):
        """
        Does the geometry for figuring out where to put and how
        to size the videos in this panel
        """
        if self.videos:
            width, height = self.GetClientSize()

            if self.orientation != wx.HORIZONTAL:
                width, height = height, width
                totalWidth = self.totalHeight
            else:
                totalWidth = self.totalWidth

            minFactor = width / float(totalWidth)
            factors = []
            xTotal = 0
            for vidPanel in self.videos:
                w, h = vidPanel.size
                if w == 0 or h == 0 : return
                if self.orientation != wx.HORIZONTAL:
                    maxFactor = float(height) / w
                    xInc = h
                else:
                    maxFactor = float(height) / h
                    xInc = w

                if maxFactor < minFactor: minFactor = maxFactor

                factor = minFactor + (maxFactor - minFactor) * self.zoom
                factors.append(factor)
                xTotal += factor * xInc

            xDelta = xTotal - width
            if xDelta < 0: xDelta = 0
            x = xDelta * self.scroll * -1
            for i, vidPanel in enumerate(self.videos):
                w, h = vidPanel.size
                factor = factors[i]
                w *= factor
                h *= factor
                vidPanel.SetSize((w, h))
                vidPanel.SetMinSize((w, h))
                vidPanel.SetMaxSize((w, h))

                extraH = float(height) - h

                if self.orientation != wx.HORIZONTAL:
                    vidPanel.SetPosition((extraH / 2, x))
                    x += h
                else:
                    vidPanel.SetPosition((x, extraH / 2))
                    x += w

    def uiUpdate(self, event=None):
        self.recalc()
        self.Refresh()

    def loadThumbs(self, filePaths):
        self.videos = []
        self.totalWidth = 0
        self.totalHeight = 0
        for path in filePaths:
            vidPanel = self.vidPanelType(self, path)
            vidPanel.loadThumb()
            self.totalWidth += vidPanel.size[0]
            self.totalHeight += vidPanel.size[1]
            self.videos.append(vidPanel)
        self.uiUpdate()

    def clear(self):
        self.DestroyChildren()
        self.videos = []

class VideoStack(wx.Panel):
    """
    A Panel that holds a stack of videos which can be scrolled and zoomed
    It has two orientations, horizontal and vertical
    """
    def __init__(self, parent, orientation, vidPanelType=None, **kwargs):
        wx.Panel.__init__(self, parent)
        self.parent = parent

        self.scrollwindow = VideoScrollPanel(self, orientation, vidPanelType, **kwargs)
        obox = wx.BoxSizer(orientation)

        def onZoom(event):
            self.scrollwindow.zoom = self.zoomControl.GetValue() / 1000.0
            self.scrollwindow.uiUpdate()

        def onScroll(event):
            self.scrollwindow.scroll = self.scrollControl.GetValue() / 1000.0
            self.scrollwindow.uiUpdate()

        if orientation == wx.HORIZONTAL:
            self.zoomControl = wx.Slider(self, wx.ID_ANY, 0, 0, 1000, style=wx.SL_VERTICAL | wx.SL_INVERSE)
            self.scrollControl = wx.Slider(self, wx.ID_ANY, 0, 0, 1000)
            obox.Add(self.zoomControl, 0, wx.EXPAND)
            obox.Add(self.scrollwindow, 1, wx.EXPAND)
            opBox = wx.BoxSizer(wx.VERTICAL)
            opBox.Add(obox, 1, wx.EXPAND)
            opBox.Add(self.scrollControl, 0, wx.EXPAND)
        else:
            self.zoomControl = wx.Slider(self, wx.ID_ANY, 0, 0, 1000)
            self.scrollControl = wx.Slider(self, wx.ID_ANY, 0, 0, 1000, style=wx.SL_VERTICAL)
            obox.Add(self.scrollwindow, 1, wx.EXPAND)
            obox.Add(self.zoomControl, 0, wx.EXPAND)
            opBox = wx.BoxSizer(wx.HORIZONTAL)
            opBox.Add(obox, 1, wx.EXPAND)
            opBox.Add(self.scrollControl, 0, wx.EXPAND)

        self.zoomControl.Bind(wx.EVT_SLIDER, onZoom)
        self.scrollControl.Bind(wx.EVT_SLIDER, onScroll)

        self.SetSizer(opBox)

    def loadThumbs(self, filePaths):
        self.scrollwindow.loadThumbs(filePaths)

    def clear(self):
        self.scrollwindow.clear()

    def bindAll(self, func):
        for vp in self.scrollwindow.videos:
            vp.Bind(wx.EVT_LEFT_UP, func)
