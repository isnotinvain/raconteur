import sys
import wx
import widgets
import uistructure

class RaconteurMainWindow(wx.Frame):
    """
    Raconteur's main UI window
    @author: Alex Levenson (alex@isnotinvain.com)
    """
    
    ABOUT = """
            Raconteur
            A Senior Design Project by Alex Levenson
            (alex@isnotinvain.com)
            Raconteur performs face tracking and face recognition 
            in video files. Raconteur hopes to become a blogging 
            utility that helps you write your video blog.
            """
    
    def __init__(self,script_path):
        wx.Frame.__init__(self, None,title="Raconteur\t|\tYour Life is a Story",size=(1500,800))
        self.__setupLayoutAndWidgets()        
        self.Show(True)
        
    def __setupLayoutAndWidgets(self):
        self.CreateStatusBar()
        
        menu_bar = wx.MenuBar()
        for menu,items in uistructure.menu:            
            wxmenu = wx.Menu()            
            for i in items:
                if len(i) == 3:
                    item,caption,callback = i
                    id = wx.ID_ANY
                elif len(i) == 4:
                    item,caption,callback,id = i
                else:
                    raise Exception("Bad menu item: "+str(i))
                
                wxItem = wxmenu.Append(id,item,caption)
                prefix = "_menu_on_"+menu.lower().replace("&","").replace(" ","")
                setattr(self.__class__,prefix+str(id),callback)
                self.Bind(wx.EVT_MENU,getattr(self,prefix+str(id)),wxItem)
            menu_bar.Append(wxmenu,menu)
        self.SetMenuBar(menu_bar)
        
        self.toolbar = wx.ToolBar(self,wx.ID_ANY,style=wx.TB_VERTICAL)
        for tool,callback in uistructure.tools:
            id = wx.NewId()
            button = wx.Button(self.toolbar, id, tool)
            setattr(self.__class__,"_toolbar_on_"+str(id),callback)
            button.Bind(wx.EVT_BUTTON,getattr(self,"_toolbar_on_"+str(id)),button)
            self.toolbar.AddControl(button)
        self.toolbar.Realize()
                
        self.videoPanel = widgets.VideoPanel(self,wx.ID_ANY)
        self.peoplePanel = widgets.PeoplePanel(self,wx.ID_ANY)        
        self.timelinePanel = widgets.TimelinePanel(self,wx.ID_ANY)
        
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.toolbar,0,wx.EXPAND)
        hsizer.SetItemMinSize(0,self.toolbar.GetMinSize())
        hsizer.Add(self.videoPanel,90,wx.EXPAND)
        hsizer.Add(self.peoplePanel,10,wx.EXPAND)
        
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(hsizer,90,wx.EXPAND)
        vsizer.Add(self.timelinePanel,10,wx.EXPAND)
        
        self.SetSizer(vsizer)
        self.SetAutoLayout(True)
                        
if __name__ == "__main__":
    app = wx.App(False)
    frame = RaconteurMainWindow(sys.argv[0])
    app.MainLoop()