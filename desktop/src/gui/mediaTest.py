import wx
import wx.media
import widgets.videoScrollPanel

class Test(wx.Frame):
    
    def __init__(self):
        wx.Frame.__init__(self, None,title="Media Control Test",size=(800,200))
        self.__setupLayoutAndWidgets()

        def quit(evt):
            #self.timer.Stop()
            evt.Skip()
            
        self.Bind(wx.EVT_CLOSE,quit)        
        self.Show(True)
           
    def __setupLayoutAndWidgets(self):        
        
        scrolio = widgets.videoScrollPanel.VideoContainer(self,wx.HORIZONTAL)
        videos = ["/media/Staggering/Raconteur/raw_data/2011/3/8/video/1299617428.mov","/media/Staggering/Raconteur/raw_data/2011/3/8/video/1299617428.mov","/media/Staggering/Raconteur/raw_data/2011/3/8/video/1299617520.mov"]
        scrolio.loadVideos(videos)        
                
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(scrolio,1,wx.EXPAND)
                
        self.SetSizer(vsizer)
        
        def test(event):
            print self.video.Tell()/float(self.video.Length())
        
        #self.timer = wx.Timer(self)
        #self.Bind(wx.EVT_TIMER,test)
        #self.timer.Start(1000.0/30.0)

if __name__ == "__main__":
    app = wx.App(False)
    Test()
    app.MainLoop()
    