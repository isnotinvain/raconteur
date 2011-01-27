'''
Created on Jan 13, 2011

@author: Alex Levenson (alex@isnotinvain.com)
'''

def rect_is_similar(rect1,rect2,similarity=0.90):
        x1,y1,w1,h1 = rect1
        x2,y2,w2,h2 = rect2
        
        wratio = float(w1)/float(w2)
        if wratio > 1: wratio = 1/wratio
        if wratio < similarity: return False
        
        hratio = float(h1)/float(h2)
        if hratio > 1: hratio = 1/hratio
        if hratio < similarity: return False
        
        wavg,havg = (w1+w2)/2.0,(h1+h2)/2.0
        
        wratio = abs(x1-x2)/wavg 

        if wratio > 1-similarity: return False
        
        hratio = abs(y1-y2)/havg
        if hratio > 1-similarity: return False
        
        return True