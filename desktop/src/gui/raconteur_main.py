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
        wx.Frame.__init__(self, None,title="Raconteur\t|\tYour Life is a Story",size=(800,500))
        
        self.CreateStatusBar()
        
        self._setup_menu()
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        split = wx.SplitterWindow(self,wx.ID_ANY,style=wx.SP_LIVE_UPDATE)
        
        sizer.Add(split,1,wx.EXPAND)
        
        tree = wx.TreeCtrl(split,wx.ID_ANY)
        panel = wx.Panel(split,wx.ID_ANY) 
        split.SplitVertically(tree,panel)
        
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.FitInside(self)
        
        
        self.Show(True)
        
    def _setup_menu(self):
        '''
        Sets up the menu bar at the top of the windo
        '''
        MENU =  (
                    ("&File",    (
                                    ("E&xit","Close Raconteur",wx.ID_EXIT),
                                )
                    ),
                            
                    ("&Import",  (
                                    ("Fi&le","Import a single file"),
                                    ("&Directory","Import a directory"),
                                )
                    ),                    
                    ("&Help",    (
                                    ("&About","About Raconteur",wx.ID_ABOUT),
                                )
                    ),
                )

        menu_bar = wx.MenuBar()
        for menu,items in MENU:            
            wxmenu = wx.Menu()            
            for i in items:
                if len(i) == 2:
                    item,caption = i
                    id = wx.ID_ANY
                else:
                    item,caption,id = i
                wxItem = wxmenu.Append(id,item,caption)
                callback = "menu_on_"+menu.lower().replace("&","")+"_"+item.lower().replace("&","")
                #if hasattr(self,callback):
                callback = getattr(self,callback)
                self.Bind(wx.EVT_MENU,callback,wxItem)
            menu_bar.Append(wxmenu,menu)
        self.SetMenuBar(menu_bar)
    
    def menu_on_file_exit(self,event):
        self.Close(True)
    
    def menu_on_import_file(self,event):
        pass
    
    def menu_on_import_directory(self,event):
        pass   
    
    def menu_on_help_about(self,event):
        dlg = wx.MessageDialog(self, self.ABOUT, "About Raconteur", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        
    def on_exit(self,event):
        self.Close(True)
        

if __name__ == "__main__":
    app = wx.App(False)
    frame = RaconteurMainWindow()
    app.MainLoop()