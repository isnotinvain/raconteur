import os
import bisect
import cPickle
import elixir
import models
import util

class Story(object):

    @classmethod
    def load(cls, path):
        f = open(os.path.join(path, ".raconteur"), "r")
        story = cPickle.load(f)
        f.close()
        story.path = path
        cls.connect(story)
        return story

    def __init__(self, name, path):
        self.path = path
        self.name = name
        self.connect()
        elixir.create_all()
        elixir.session.commit()

    def commit(self):
        elixir.session.commit()

    def connect(self):
        elixir.metadata.bind = "sqlite+pysqlite:///" + os.path.join(self.path, ".raconteur-db.sql")
        elixir.metadata.bind.echo = False
        elixir.setup_all()

    def save(self):
        util.filesystem.ensureDirectoryExists(self.path)
        f = open(os.path.join(self.path, ".raconteur"), "w")
        cPickle.dump(self, f)
        f.close()

    def getStreamsInRange(self, start, end, streamType):
        creations = self.stream_creations[streamType]
        s = bisect.bisect_left(creations, start)
        if s == len(creations): return []

        e = bisect.bisect_right(creations, end)
        if not e: return []

        return map(lambda x : (x, self.stream_files[streamType][x]), creations[s:e])

    def addPerson(self, name):
        models.Person(name=name)
        elixir.session.commit()

    def getPeopleDir(self):
        return os.path.join(self.path, ".people")

    def getUnrecognizedPeopleDir(self):
        return os.path.join(self.getPeopleDir(), "unrecognized")

    def getPersonDir(self, name):
        if not models.Person.get(name):
            self.addPerson(name)
        return os.path.join(self.getPeopleDir(), name)
