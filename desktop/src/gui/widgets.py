'''
Created on Feb 3, 2011

@author: Alex Levenson (alex@isnotinvain.com)
'''
import wx
class NewStoryDialog(wx.Dialog):
    def __init__(self, parent, id,**kwargs):
        kwargs['title'] = "Create a New Story"
        wx.Dialog.__init__(self, parent, id,**kwargs)
        
        pvbox = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, wx.ID_ANY)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        dirLabel = wx.StaticText(panel,wx.ID_ANY,label="Enter a directory to store Raconteur's data:")        
        self.directoryCtrl = wx.TextCtrl(panel, wx.ID_ANY)
        
        nameLabel = wx.StaticText(panel,wx.ID_ANY,label="Enter a name for this story:")        
        self.nameCtrl = wx.TextCtrl(panel, wx.ID_ANY)
        
        pvbox.Add(dirLabel,0,wx.EXPAND)
        pvbox.Add(self.directoryCtrl,0,wx.EXPAND)
        pvbox.Add(nameLabel,0,wx.EXPAND)
        pvbox.Add(self.nameCtrl,0,wx.EXPAND)
        panel.SetSizer(pvbox)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, wx.ID_OK, "Create!") 
        hbox.Add(okButton, 1)        

        vbox.Add(panel)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        self.SetSizer(vbox)
        vbox.Fit(self)

class OpenStoryDialog(wx.Dialog):
    def __init__(self, parent, id,**kwargs):
        kwargs['title'] = "Open a Story"
        wx.Dialog.__init__(self, parent, id,**kwargs)
        
        pvbox = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, wx.ID_ANY)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        dirLabel = wx.StaticText(panel,wx.ID_ANY,label="Enter the path to the root of the story")        
        self.directoryCtrl = wx.TextCtrl(panel, wx.ID_ANY)
        
        
        pvbox.Add(dirLabel,0,wx.EXPAND)
        pvbox.Add(self.directoryCtrl,0,wx.EXPAND)
        panel.SetSizer(pvbox)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, wx.ID_OK, "Open") 
        hbox.Add(okButton, 1)        

        vbox.Add(panel)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        self.SetSizer(vbox)
        vbox.Fit(self)