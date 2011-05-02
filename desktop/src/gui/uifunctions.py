'''
Raconteur (c) Alex Levenson 2011
All rights reserved

@author: Alex Levenson (alex@isnotinvain.com)

Functions that get linked into RaconteurMainWindow
I wanted to keep the UI layout and functionality seperate 
'''

import os
import shutil
import fnmatch
import cPickle
import wx
import cv
import widgets
import widgets.video_overlays
import stream.story
import stream.importer
import stream.models
import vision.finder
import vision.tracker
import vision.recognizer
import util.filesystem

def checkStory(self, evnt=None):
    if not self.story:
        d = wx.MessageDialog(self, "You need to open a story first!", "Wooops!", wx.OK)
        d.ShowModal()
        d.Destroy()
        return False
    return True

def onImport(self, event):
    if not checkStory(self): return
    d = widgets.ImportDialog(self, wx.ID_ANY)
    if d.ShowModal() == wx.ID_OK:
        streamType = d.streamTypeCtrl.GetValue()
        directory = d.directoryCtrl.GetValue()
        regex = d.regexCtrl.GetValue()
        d.Destroy()
        db_type = None
        if streamType == "video": db_type = stream.models.Video

        imp = stream.importer.StreamImporter(streamType, self.story.path, d.moveCheck.GetValue(), db_type)
        progDialog = wx.ProgressDialog("Importing", "Importing...", maximum=1000, parent=self, style=wx.PD_CAN_ABORT)
        filter = lambda x : fnmatch.fnmatch(x, regex)
        try:
            imp.importDirectory(directory, progDialog=progDialog, filter_function=filter)
        except stream.importer.NoSuchDirectoryError:
            widgets.misc.messageBox(self, "Directory does not exist:\n" + directory, "Woops!")
            progDialog.Destroy()
            return
        self.story.commit()
        progDialog.Destroy()
        self.reloadTimeline()
        self.Refresh()
    else: d.Destroy()

def onAnalyze(self, event):
    d = widgets.AnalyzeDialog(self, wx.ID_ANY)
    if d.ShowModal() == wx.ID_OK:
        faceFind = d.faceCheck.GetValue()
        if faceFind:
            faceScale = eval(d.faceScale.GetValue())
            faceParams = eval(d.faceParams.GetValue())

        faceTrack = d.trackCheck.GetValue()
        if faceTrack:
            trackParams = eval(d.trackParams.GetValue())

        faceExtract = d.extractCheck.GetValue()
        if faceExtract:
            extractParams = eval(d.extractParams.GetValue())

        faceRecognize = d.recognizeCheck.GetValue()
        if faceRecognize:
            recognizeParams = eval(d.recognizeParams.GetValue())

        d.Destroy()

        if faceFind:
            video = vision.video.CvVideo(self.currentVideo)
            if faceScale:
                finder = vision.finder.ObjectFinder(scaleTo=faceScale)
            else:
                finder = vision.finder.ObjectFinder()
            progDialog = wx.ProgressDialog("Extracting Face Boundaries", "Working...", maximum=1000, parent=self, style=wx.PD_CAN_ABORT)
            video.face_bounds = finder.findInVideo(video, progDialog=progDialog, **faceParams)
            video.writeFaceBounds()
            progDialog.Destroy()
            video = None

        if faceTrack:
            video = vision.video.CvVideo(self.currentVideo)
            dbVideo = stream.models.Video.get(video.file_path)
            stream.models.PersonAppearance.query.filter_by(video=dbVideo).delete()
            self.story.commit()

            video.loadFaceBounds()
            tracker = vision.tracker.ObjectTracker(**trackParams)
            face_tracks = tracker.extractAndInerpolateTracks(video.face_bounds)
            unrecognized = self.story.getUnrecognizedPerson()
            dbVideo = stream.models.Video.get(video.file_path)
            for track in face_tracks:
                track = cPickle.dumps(track)
                stream.models.PersonAppearance(track=track, person=unrecognized, video=dbVideo)
            video = None
            self.story.commit()

        if faceExtract:
            video = vision.video.CvVideo(self.currentVideo)
            video.loadFaceBounds()
            dbVideo = stream.models.Video.get(video.file_path)
            for x in stream.models.PersonAppearance.query.filter_by(video=dbVideo).all():
                x.faces = None
            self.story.commit()

            dbTracks = dbVideo.getDbTracks()
            tracks = [(x.id, cPickle.loads(str(x.track))) for x in dbTracks]
            idToDb = dict((x.id, x) for x in dbTracks)

            video.calcDuration()
            progDialog = wx.ProgressDialog("Extracting Faces", "Working...", maximum=video.getNormalizedFrameCount(), parent=self, style=wx.PD_CAN_ABORT)
            faceTracks, numFaces = vision.tracker.ObjectTracker.getFacesFromTracks(video, tracks, progDialog)
            progDialog.Destroy()

            progDialog = wx.ProgressDialog("Saving Faces", "Working...", maximum=numFaces, parent=self, style=wx.PD_CAN_ABORT)
            prog = 0
            root = os.path.join(self.story.getUnrecognizedPeopleDir(), video.creation)
            util.filesystem.ensureDirectoryExists(root)
            for fl in os.listdir(root):
                os.remove(os.path.join(root, fl))

            for id, faces in faceTracks.iteritems():
                filename = root + "/" + str(id) + ".avi"
                writer = cv.CreateVideoWriter(filename, cv.CV_FOURCC('P', 'I', 'M', '1'), video.getFps(), extractParams['scaleTo'], True)
                for face in faces:
                    cont, _ = progDialog.Update(prog, "Saving Faces")
                    if not cont:
                        progDialog.Destroy()
                        video = None
                        return
                    scaled = cv.CreateImage(extractParams['scaleTo'], face.depth, face.nChannels)
                    cv.Resize(face, scaled, cv.CV_INTER_LINEAR)
                    cv.WriteFrame(writer, scaled)
                    prog += 1
                idToDb[id].faces = filename

            self.story.commit()
            progDialog.Destroy()
            video = None

def onShowOverlays(self, event):
    bounds = False
    tracks = False
    recognize = False

    video = vision.video.CvVideo(self.currentVideo)
    dbVideo = stream.models.Video.get(video.file_path)

    try:
        video.loadFaceBounds()
        bounds = True
    except:
        pass

    faceTracks = dbVideo.getTracks()
    if faceTracks: tracks = True

    d = widgets.ShowOverlaysDialog(self, wx.ID_ANY, bounds, tracks, recognize)
    if d.ShowModal() == wx.ID_OK:
        if bounds:
            bounds = d.faceCheck.GetValue()
        if faceTracks:
            tracks = d.trackCheck.GetValue()
        if recognize:
            recognize = d.extractCheck.GetValue()
        d.Destroy()

        self.videoPanel.overlays = []

        if bounds:
            overlay = widgets.video_overlays.overlayFromFaceBounds(video.face_bounds)
            self.videoPanel.overlays.append(overlay)
        if tracks:
            overlay = widgets.video_overlays.overlayFromTracks(faceTracks, video.face_bounds)
            self.videoPanel.overlays.append(overlay)

        video = None
    else: d.Destroy()

def onNewStory(self, event):
    d = widgets.NewStoryDialog(self, wx.ID_ANY)
    if d.ShowModal() == wx.ID_OK:
        path = d.directoryCtrl.GetValue()
        name = d.nameCtrl.GetValue()
        story = stream.story.Story(name, path)
        story.save()
        self.loadStory(path)
    d.Destroy()

def onOpenStory(self, event):
    d = wx.DirDialog(self, message="Open A Story", style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
    if d.ShowModal() == wx.ID_OK:
        self.loadStory(d.GetPath())
    d.Destroy()

def onExit(self, event):
    self.Close()

def onAbout(self, event):
    d = wx.MessageDialog(self, self.ABOUT, "About Raconteur", wx.OK)
    d.ShowModal()
    d.Destroy()

def onPlayPause(self, event):
    self.videoPanel.playPause()

def onReset(self, event):
    self.videoPanel.stop()
    self.videoPanel.overlays = []

def onReTrain(self, event=None):
    d = wx.TextEntryDialog(self, message="How many frames per face video should I skip?")
    d.SetValue("10")
    skipNFrames = None
    if d.ShowModal() == wx.ID_OK:
        skipNFrames = int(d.GetValue())
    else:
        d.Destroy()
        return

    d.Destroy()

    if skipNFrames:
        ids = vision.recognizer.train(self.story.getPeopleDir(), skipNFrames)
    else:
        ids = vision.recognizer.train(self.story.getPeopleDir())

    f = open(os.path.join(self.story.getPeopleDir(), ".trainingData", ".ids"), "w")
    cPickle.dump(ids, f)
    f.close()

def onRecognize(self, event):
    d = wx.MessageDialog(self, "Should I Recalculate the training data?", "Recognize", wx.YES_NO)
    if d.ShowModal() == wx.ID_YES:
        d.Destroy()
        onReTrain(self)
    else:
        d.Destroy()

    unrecognized = stream.models.PersonAppearance.query.filter_by(person=self.story.getUnrecognizedPerson()).all()
    for face in unrecognized:
        hist, total = vision.recognizer.recognize(self.story.getPeopleDir(), face.faces)
        best = max(hist.itervalues())
        for k, v in hist.iteritems():
            if v == best:
                break
        person = stream.models.Person.get(k)
        app = stream.models.PersonAppearance.get_by(faces=face.faces)
        dest = self.story.getPersonDir(k)
        util.filesystem.ensureDirectoryExists(dest)
        dest = os.path.join(dest, util.filesystem.generateUniqueFileName(dest, ".avi"))
        shutil.move(face.faces, dest)

        app.manuallyTagged = False
        app.certaintyHistogram = cPickle.dumps((hist, total))
        app.person = person
        app.faces = dest
        self.story.commit()

def onTrain(self, event):
    d = None
    add = lambda x, y : onAddFace(self, d, x, y)
    dell = lambda x : onDelFace(self, d, x)
    d = widgets.ManageFaces(self, self.story.getUnrecognizedPerson(), add, dell)
    d.Show()

def onManagePerson(self, event):
    d = None
    add = lambda x, y : onAddFace(self, d, x, y)
    dell = lambda x : onDelFace(self, d, x)
    person = stream.models.PersonAppearance.get_by(faces=event.EventObject.path).person
    d = widgets.ManageFaces(self, person, add, dell)
    d.Show()

def onAddFace(self, d, path, name):
    person = self.story.addPerson(name)
    appearance = stream.models.PersonAppearance.get_by(faces=path)

    dest = self.story.getPersonDir(name)
    util.filesystem.ensureDirectoryExists(dest)
    dest = os.path.join(dest, util.filesystem.generateUniqueFileName(dest, ".avi"))
    shutil.move(path, dest)

    appearance.person = person
    appearance.faces = dest
    appearance.manuallyTagged = True
    appearance.certaintyHistogram = None
    self.story.commit()
    d.crawl()
    self.reloadPeoplePanel()

def onDelFace(self, d, path):
    appearance = stream.models.PersonAppearance.get_by(faces=path)
    if not appearance:
        print "didn't find :%s" % path
        return
    appearance.delete()
    os.remove(path)
    self.story.commit()
    d.crawl()
    self.reloadPeoplePanel()

tools = (
            ("Import", onImport),
            ("Analyze", onAnalyze),
            ("Visualize", onShowOverlays),
            ("Train", onTrain),
            ("Recognize", onRecognize),
            ("Play", onPlayPause)
        )

extra = ((onManagePerson, "onManagePerson"),)

menu = (
            ("&File", (
                            ("&New Story", "Create a new story", onNewStory),
                            ("&Open Story", "Open a new story", onOpenStory),
                            ("E&xit", "Close Raconteur", onExit, wx.ID_EXIT),
                        )
            ),
            ("&Playback", (
                            ("&Play / Pause", "Play or Pause the current video", onPlayPause),
                            ("&Reset", "Reset the current video", onReset),
                        )
            ),
            ("&Help", (
                            ("&About", "About Raconteur", onAbout, wx.ID_ABOUT),
                        )
            ),
        )
