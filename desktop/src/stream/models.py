from elixir import *
from sqlalchemy.ext.associationproxy import AssociationProxy
import cPickle

class Person(Entity):
    name = Field(Text(), primary_key=True, required=True, unique=True)
    person_appearances = OneToMany('PersonAppearance')
    appearsIn = AssociationProxy('person_appearances', 'video')

    def __repr__(self):
        return '<Person: "%s">' % (self.name)

class Video(Entity):
    path = Field(Text(), primary_key=True, required=True, unique=True)
    creation = Field(Integer(), required=True)
    person_appearances = OneToMany('PersonAppearance')
    people = AssociationProxy('person_appearances', 'person')

    def getTracks(self):
        return map(lambda x : cPickle.loads(str(x.track)), PersonAppearance.query.filter_by(video=self).all())

    def getDbTracks(self):
        return PersonAppearance.query.filter_by(video=self).all()

    def __repr__(self):
        return '<Video: "%s">' % (self.path)

class PersonAppearance(Entity):
    track = Field(Text(), required=True)
    person = ManyToOne("Person", required=True)
    video = ManyToOne("Video", required=True)
    faces = Field(Text())
    #manual = Field(Boolean())

    def getTrack(self):
        return cPickle.loads(str(x.track))

    def __repr__(self):
        return '<PersonAppearance: %s <-> %s' % (self.person, self.video)
