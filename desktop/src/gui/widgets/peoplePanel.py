'''
Created on Feb 3, 2011

@author: Alex Levenson (alex@isnotinvain.com)
'''
import os
import wx
import stream.video
import vision.recognizer
import util.image
from gui.widgets.dialogs import ManageAFaceDialog
import shutil
import util.filesystem

class PeoplePanel(wx.Panel):
    '''
    A panel that draws the faces of recognized people
    in a vertical stack
    '''
    def __init__(self,parent,id,**kwargs):
        wx.Panel.__init__(self,parent,id,**kwargs)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_SIZE, self.onPaint)
        self.Bind(wx.EVT_LEFT_UP,self.onClick)
        self.bgBrush = wx.Brush((240,240,240))        
        self.bgPen = wx.TRANSPARENT_PEN
        self.videoPen = wx.Pen((100,100,100),2)
        self.videoBrush = wx.TRANSPARENT_BRUSH
        self.parent = parent
        self.faceVideos = []
        self.thumbs = []
        self.thumbSize = None
        self.zoom = 0.0
        self.pos = 0.0
        self.videoRects = None
        self.timer = wx.Timer(self, wx.ID_ANY)
        self.timer_tick = 1000/10
        self.Bind(wx.EVT_TIMER,self.onNextFrame)
        self.totalHeight = None
        self.playing = False

    def loadPeople(self):
        peopleDir = os.path.join(self.parent.story.getUnrecognizedPeopleDir(),self.parent.currentVideo.creation)
        if os.path.exists(peopleDir):
            self.faceVideos = []
            for v in os.listdir(peopleDir):
                if v[0] == ".": continue
                self.faceVideos.append(stream.video.Video(os.path.join(peopleDir,v)))
            
            if len(self.faceVideos) > 0:
                w = self.faceVideos[0].getNextFrame().width
                self.faceVideos[0].reset()
                self.thumbSize = w
                self.totalHeight = len(self.faceVideos)*self.thumbSize
                self.onNextFrame(None)
                self.Refresh()
        else:
            self.faceVideos = []
        
    def pause(self,event=None):
        self.timer.Stop()
        self.playing = False
    
    def play(self,event=None):
        self.timer.Start(self.timer_tick)
        self.playing = True
    
    def playPause(self,event=None):
        if self.playing: self.pause()        
        else: self.play()
    
    def onClick(self,event):
        if not self.videoRects: return
        pt = event.m_x,event.m_y
        rect = util.geometry.pointInWhichRect(pt, self.videoRects.iterkeys())
        if rect == None: return
        video = self.videoRects[rect]
        wasPlaying = self.playing
        self.pause()
        d=ManageAFaceDialog(self,wx.ID_ANY,video)
        action = d.ShowModal()
        if action == ManageAFaceDialog.ADD_FACE:
            name = d.nameCtrl.GetValue()            
            dest = self.parent.story.getPersonDir(name)
            util.filesystem.ensureDirectoryExists(dest)
            dest = os.path.join(dest,util.filesystem.generateUniqueFileName(dest,".avi"))
            shutil.move(video.file_path,dest)
        elif action == ManageAFaceDialog.DEL_FACE:
            self.faceVideos.remove(video)
            os.remove(video.file_path)
        elif action == ManageAFaceDialog.RECOG_FACE:
            hist = vision.recognizer.recognize(self.parent.story.getPeopleDir(), video)
            print hist            
            
        d.Destroy()
        self.loadPeople()
        if wasPlaying: self.play()
    
    def setZoom(self,zoom):
        self.zoom = zoom
        
    def setPos(self,pos):
        self.pos = pos

    def onNextFrame(self,event):
        self.thumbs = []
        for video in self.faceVideos:
            thumb = video.getNextFrame()
            if not thumb: 
                video.reset()
                thumb = video.getNextFrame()
            self.thumbs.append((thumb,video))
        self.Refresh()
        
    def onPaint(self,event):
        dc = wx.AutoBufferedPaintDC(self)
        dcW,dcH = dc.GetSize()
        if dcW < 0 or dcH < 0: return

        dc.Clear()
        dc.SetBrush(self.bgBrush)
        dc.SetPen(self.bgPen)
        dc.DrawRectangle(0,0,dcW,dcH)
        dc = wx.AutoBufferedPaintDC(self)

        if not self.faceVideos: return
        
        dc.SetPen(self.videoPen)        
        dc.SetBrush(self.videoBrush)
        
        minScaleFactor = dcH / float(self.totalHeight)
        maxScaleFactor = dcW / float(self.thumbSize)
        deltaScale = maxScaleFactor - minScaleFactor        
        scaleFactor = minScaleFactor + self.zoom*deltaScale
         
        pplHeight = self.totalHeight*scaleFactor
        deltaOffset = pplHeight - dcH
        y = -1 * deltaOffset * self.pos
        
        self.videoRects = {}
        for thumb,video in self.thumbs:            
            img = util.image.cvToWx(thumb)
            fitsize = dcW,scaleFactor*self.thumbSize
            scaledWidth,scaledHeight = util.geometry.getScaledDimensions(img.GetSize(),fitsize)            
            img = img.Scale(scaledWidth,scaledHeight,wx.IMAGE_QUALITY_NORMAL)
            img = wx.BitmapFromImage(img)
            
            x = dcW/2.0 - (scaledWidth/2.0)
            
            dc.DrawBitmap(img,x,y)
            rect = (x,y,scaledWidth,scaledHeight)
            self.videoRects[rect] = video
            dc.DrawRectangle(*rect)
            y+=scaledHeight