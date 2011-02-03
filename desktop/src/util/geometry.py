'''
Created on Jan 13, 2011

@author: Alex Levenson (alex@isnotinvain.com)

Geometry utility functions
'''

def rect_contain(rect1,rect2):
    """
    Returns whether rect1 contains rect2
    """
    x1,y1,w1,h1 = rect1
    x2,y2,w2,h2 = rect2

    if x2 >= x1 and y2 >= y1 and x2 <= x1+w1 and y2 <= y1+h1 and x2+w2 <= x1+w1 and y2+h2 <= y1+h1:
        return True
    return False

def rect_is_similar(rect1,rect2,similarity):
    """
    Returns whether rect1 and rect2 are 'similar' by the similarity threshold
    """
    x1,y1,w1,h1 = rect1
    x2,y2,w2,h2 = rect2
    
    if rect_contain(rect1,rect2): return True    
    if rect_contain(rect2,rect1): return True
    
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