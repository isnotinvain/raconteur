'''
Raconteur (c) Alex Levenson 2011
All rights reserved

@author: Alex Levenson (alex@isnotinvain.com)

Geometry utility functions
'''

import math

def distance(self, x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def getTweenedVector(fromRect, toRect, numFrames):
    floatFrames = float(numFrames)

    tweenRect = list(fromRect)

    deltas = map(lambda x : x[1] - x[0], zip(fromRect, toRect))
    deltas = map(lambda x : x / floatFrames, deltas)

    frames = []
    for _ in xrange(numFrames - 1):
        tweenRect = map(lambda x: x[1] + deltas[x[0]], enumerate(tweenRect))
        frames.append(tuple(tweenRect))
    return frames

def getScaledDimensions(size, max_size, returnFactor=False):
    """
    @return a rectangle scaled to fit inside max_size while preserving aspect ratio
    """

    width, height = size
    max_width, max_height = max_size
    if (max_width, max_height) == (0, 0) or (width, height) == (0, 0): return (0, 0)
    wfactor, hfactor = 1.0, 1.0

    if width > max_width: wfactor = float(max_width) / width
    if height > max_height: hfactor = float(max_height) / height

    factor = min(wfactor, hfactor)

    size = (width * factor, height * factor)

    if not returnFactor:
        return size
    else:
        return size, factor

def rectContains(rect1, rect2):
    """
    @return whether rect1 contains rect2
    """
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2

    if x2 >= x1 and y2 >= y1 and x2 <= x1 + w1 and y2 <= y1 + h1 and x2 + w2 <= x1 + w1 and y2 + h2 <= y1 + h1:
        return True
    return False

def rectIsSimilar(rect1, rect2, similarity):
    """
    @return whether rect1 and rect2 are 'similar' by the similarity threshold
    """
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2

    if rectContains(rect1, rect2): return True
    if rectContains(rect2, rect1): return True

    wratio = float(w1) / float(w2)
    if wratio > 1: wratio = 1 / wratio
    if wratio < similarity: return False

    hratio = float(h1) / float(h2)
    if hratio > 1: hratio = 1 / hratio
    if hratio < similarity: return False

    wavg, havg = (w1 + w2) / 2.0, (h1 + h2) / 2.0

    wratio = abs(x1 - x2) / wavg

    if wratio > 1 - similarity: return False

    hratio = abs(y1 - y2) / havg
    if hratio > 1 - similarity: return False

    return True

def pointInRect(pt, rect):
    px, py = pt
    rx, ry, w, h = rect
    return px >= rx and px <= rx + w and py >= ry and py <= ry + h

def pointInWhichRect(pt, rects):
    for rect in rects:
        if pointInRect(pt, rect): return rect
    return None
