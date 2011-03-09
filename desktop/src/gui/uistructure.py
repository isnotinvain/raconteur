def onImport(self,event):
    print "import"
    
def onAnalyze(self,event):
    print "analyze"
    
tools = (
            ("Import", onImport),
            ("Analyze", onAnalyze)
        )