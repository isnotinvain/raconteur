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
        self.commit()

    def commit(self):
        elixir.session.commit()

    def connect(self):
        elixir.metadata.bind = "sqlite+pysqlite:///" + self.getDbPath()
        elixir.metadata.bind.echo = False
        elixir.setup_all()

    def getDbPath(self): return os.path.join(self.path, ".raconteur-db.sql")

    def save(self):
        util.filesystem.ensureDirectoryExists(self.path)
        f = open(os.path.join(self.path, ".raconteur"), "w")
        cPickle.dump(self, f)
        f.close()

    def addPerson(self, name):
        models.Person(name=name)
        self.commit()

    def getPeopleDir(self):
        return os.path.join(self.path, ".people")

    def getUnrecognizedPeopleDir(self):
        return os.path.join(self.getPeopleDir(), "unrecognized")

    def getPersonDir(self, name):
        if not models.Person.get(name):
            self.addPerson(name)
        return os.path.join(self.getPeopleDir(), name)

    def clearDb(self):
        if os.path.exists(self.getDbPath()): os.remove(os.path.join(self.path, ".raconteur-db.sql"))
        self.connect()
        elixir.create_all()

    def recrawl(self, streamType, streamDbType):
        hdPaths = {}
        for root, _, files in os.walk(self.path):
            if root[root.rfind("/") + 1:] == streamType:
                for file in files:
                    if file[0] == ".": continue
                    creation_stamp = int(file[:file.rfind('.')])
                    fpath = os.path.join(root, file)
                    hdPaths[fpath] = creation_stamp

        dbStreams = streamDbType.query.all()
        dbPaths = map(lambda x : x.path, dbStreams)

        missing = [x for x in dbStreams if x.path not in hdPaths]
        for m in missing:
            m.delete()

        new = [(p, c) for p, c in hdPaths.iteritems() if p not in dbPaths]
        for p, c in new:
            streamDbType(path=p, creation=c)

        self.commit()
