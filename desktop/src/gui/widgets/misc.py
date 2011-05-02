'''
Raconteur (c) Alex Levenson 2011
All rights reserved

@author: Alex Levenson (alex@isnotinvain.com)

Miscelaneous widgets
'''

import wx

def messageBox(parent, message, title):
    """
    Convenience function for modal message boxes
    """
    d = wx.MessageDialog(parent, message, title, wx.OK)
    d.ShowModal()
    d.Destroy()
