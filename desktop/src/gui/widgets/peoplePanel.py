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
        self.bgBrush = wx.Brush((100,100,200)) 
            
    def onPaint(self,event):
        dc = wx.PaintDC(self)
        dcW,dcH = dc.GetSize()
        if dcW < 0 or dcH < 0: return
        
        dc.Clear()
        dc.SetBrush(self.bgBrush)
        dc.SetPen(wx.TRANSPARENT_PEN)        
        dc.DrawRectangle(0,0,dcW,dcH)