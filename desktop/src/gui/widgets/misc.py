import wx

def messageBox(parent,message,title):
    d = wx.MessageDialog(parent,message,title,wx.OK)
    d.ShowModal()
    d.Destroy()