'''
Created on Feb 3, 2011

@author: Alex Levenson (alex@isnotinvain.com)
'''

class ProgressTracker(object):
    """
    Used for tracking progress in slow operations
    """
    def __init__(self,callback,currentProcess="Working..."):
        self.currentProcess = currentProcess
        self.progress = 0.0
        self.tickAmount = 0.0
        self.abort = False
        self.callback = callback

    def requestAbort(self):
        self.abort = True
        
    def tick(self,value=None):
        if not value:
            self.progress+=self.tickAmount
        else:
            self.progress=value
        self.callback(self.progress)
        
    def isDone(self):
        return self.progress >= 1.0