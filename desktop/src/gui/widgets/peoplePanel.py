'''
Created on Feb 3, 2011

@author: Alex Levenson (alex@isnotinvain.com)
'''
import wx

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

    def loadPeople(self):
        pass
    
    def onClick(self,event):
        pass
            
    def onPaint(self,event):
        dc = wx.AutoBufferedPaintDC(self)
        dcW,dcH = dc.GetSize()
        if dcW < 0 or dcH < 0: return

        dc.Clear()
        dc.SetBrush(self.bgBrush)
        dc.SetPen(self.bgPen)
        dc.DrawRectangle(0,0,dcW,dcH)
