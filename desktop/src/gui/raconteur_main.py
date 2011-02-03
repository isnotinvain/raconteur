'''
Created on Feb 2, 2011

@author: Alex Levenson (alex@isnotinvain.com)
'''
import wx

class RaconteurMainWindow(wx.Frame):
    '''
    The main GUI class for Raconteur
    '''
    ABOUT = """
    Raconteur
    A Senior Design Project by Alex Levenson
    (alex@isnotinvain.com)
    Raconteur performs face tracking and face recognition 
    in video files. Raconteur hopes to become a blogging 
    utility that helps you write your video blog.
    """
            
    def __init__(self):
        wx.Frame.__init__(self, None,title="Raconteur\t|\tYour Life is a Story", size=(700,500))
        
        self.CreateStatusBar()
        
        self._setup_menu()
        
        self.Show(True)
        
    def _setup_menu(self):
        '''
        Sets up the menu bar at the top of the windo
        '''
        # setup the file menu
        file_menu = wx.Menu()
        about = file_menu.Append(wx.ID_ABOUT, "&About","About Raconteur")
        file_menu.AppendSeparator()
        exit = file_menu.Append(wx.ID_EXIT,"E&xit","Close Raconteur")
        
        self.Bind(wx.EVT_MENU, self.on_about, about)
        self.Bind(wx.EVT_MENU, self.on_exit, exit)

        # setup the menu bar
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu,"&File")
        self.SetMenuBar(menu_bar)
    
    def on_about(self,event):
        dlg = wx.MessageDialog(self, self.ABOUT, "About Raconteur", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        
    def on_exit(self,event):
        self.Close(True)
        

if __name__ == "__main__":
    app = wx.App(False)
    frame = RaconteurMainWindow()
    app.MainLoop()