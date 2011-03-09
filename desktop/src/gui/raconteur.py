ABOUT = """
Raconteur
A Senior Design Project by Alex Levenson
(alex@isnotinvain.com)
Raconteur performs face tracking and face recognition 
in video files. Raconteur hopes to become a blogging 
utility that helps you write your video blog.
"""

import sys
import wx
import uistructure

class RaconteurMainWindow(wx.Frame):
    """
    Raconteur's main UI window
    @author: Alex Levenson (alex@isnotinvain.com)
    """
    def __init__(self,script_path):
        wx.Frame.__init__(self, None,title="Raconteur\t|\tYour Life is a Story",size=(800,500))
        self.__setupLayoutAndWidgets()
        
        self.Show(True)
    
    def __setupLayoutAndWidgets(self):
        self.CreateStatusBar()
        toolbar = self.CreateToolBar(wx.TB_VERTICAL)
        
        for tool,callback in uistructure.tools:
            id = wx.NewId()
            button = wx.Button(toolbar, id, tool)
            setattr(self.__class__,"_toolbar_on_"+str(id),callback)
            button.Bind(wx.EVT_BUTTON,getattr(self,"_toolbar_on_"+str(id)),button)
            toolbar.AddControl(button)
            
                        
if __name__ == "__main__":
    app = wx.App(False)
    frame = RaconteurMainWindow(sys.argv[0])
    app.MainLoop()