import util.image

def getFacesFromTracks(video,progDialog=None):    
    faces = {}
    for track in video.face_tracks:
        faces[id(track)] = []
        
    for frameNo,frame in enumerate(video.frames()):
            for track in video.face_tracks:
                if frameNo in track:
                    face = util.image.getCvSubRect(frame, track[frameNo])
                    
                    faces[id(track)].append(face)                    
                    if progDialog:
                        cont,_ = progDialog.Update(frameNo,"Extracting faces...")
                        if not cont: return
    return faces.values()