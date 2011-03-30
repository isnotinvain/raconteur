'''
(c) Alex Levenson 2010 | alex@isnotinvain.com | Raconteur

@author: Alex Levenson (alex@isnotinvain.com)
'''

import util.geometry
import util.image

class ObjectTracker(object):
    """
    Tracks objects through a video stream
    """
    def __init__(self, look_ahead_threshold=10, similarity=0.75, min_track_size=10):
        self.look_ahead_threshold = look_ahead_threshold
        self.similarity = similarity
        self.min_track_size = min_track_size

    def _trackBound(self, raw_bounds, tracked, bound, f):
        """
        Track a single bound through the video
        """
        track = {}
        track[f] = bound
        miss_count = 0
        frame_count = 0
        while miss_count <= self.look_ahead_threshold:
            miss = True
            if f + frame_count >= len(raw_bounds): break
            for b, _ in raw_bounds[f + frame_count]:
                if (f + frame_count, b) in tracked: continue
                if util.geometry.rectIsSimilar(b, bound, self.similarity):
                    track[f + frame_count] = b
                    bound = b
                    miss_count = 0
                    miss = False
                    break
            if miss:
                miss_count += 1
            frame_count += 1
        return track

    def extractTracks(self, raw_bounds, progDialog=None, progressUpdateRate=100):
        """
        The main algorithm of the ObjectTracker,
        Crawls through the raw object bounds and tries
        to guess which bounds correspond to the same object
        across frames, using locality
        """
        tracks = []
        tracked = set()
        for f, frame_bounds in enumerate(raw_bounds):
            for bound, _ in frame_bounds:
                if (f, bound) in tracked: continue
                track = self._trackBound(raw_bounds, tracked, bound, f)
                if len(track) > self.min_track_size:
                    tracks.append(track)
                    for t in track.iteritems():
                        tracked.add(t)
            if progDialog and f % progressUpdateRate == 0:
                cont, _ = progDialog.Update(f, "Extracting Face Boundaries...")
                if not cont: return tracks
                pass
        return tracks

    def interpolateTracks(self, tracks):
        """
        Scans through each track and makes it continuous by filling in frames that are missing.
        When a series of missing frames is found, it is filled in with a tween from the frame
        before the gap to the frame that ends the gap
        """
        for track in tracks:
            frames = sorted(track)
            lastFrame = frames[0]
            for frameNo in frames[1:]:
                if frameNo != lastFrame + 1:
                    tween = util.geometry.getTweenedVector(track[lastFrame], track[frameNo], frameNo - lastFrame)
                    #print "gap: "+str(lastFrame)+": " + str(track[lastFrame]) + " -- " + str(frameNo)+": " + str(track[frameNo])
                    #print tween
                    for i, rect in enumerate(tween):
                        track[lastFrame + i] = tween[i]
                lastFrame = frameNo

    def extractAndInerpolateTracks(self, raw_bounds, progDialog=None, progressUpdateRate=100):
        tracks = self.extractTracks(raw_bounds, progDialog, progressUpdateRate)
        self.interpolateTracks(tracks)
        return tracks

    @classmethod
    def getFacesFromTracks(cls, video, progDialog=None):
        faces = {}
        for track in video.face_tracks:
            faces[id(track)] = []

        for frameNo, frame in enumerate(video.frames()):
                for track in video.face_tracks:
                    if frameNo in track:
                        face = util.image.getCvSubRect(frame, track[frameNo])
                        faces[id(track)].append(face)
                        if progDialog:
                            cont, _ = progDialog.Update(frameNo, "Extracting faces...")
                            if not cont: return
        return faces.values()
