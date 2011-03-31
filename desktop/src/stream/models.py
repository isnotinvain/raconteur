from elixir import *
from sqlalchemy.ext.associationproxy import AssociationProxy

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

    def __repr__(self):
        return '<Video: "%s">' % (self.path)

class PersonAppearance(Entity):
    track = Field(Text(), required=True)
    person = ManyToOne("Person")
    video = ManyToOne("Video")

    def __repr__(self):
        return '<PersonAppearance: %s <-> %s : %d' % (self.person, self.video, self.trackID)

#import os
#if os.path.exists("/home/alex/Desktop/tttmp.sql"): os.remove("/home/alex/Desktop/tttmp.sql")
#
#metadata.bind = "sqlite+pysqlite:////home/alex/Desktop/tttmp.sql"
#metadata.bind.echo = False
#setup_all(True)
#
#people = []
#videos = []
#for p in ("Alex", "Toy", "Dean"):
#    people.append(Person(name=p))
#
#for i, v in enumerate(("at", "td", "d", "atd")):
#    videos.append(Video(path=v, creation=i))
#
#PersonAppearance(track="0", person=people[0], video=videos[0])
#PersonAppearance(track="w", person=people[0], video=videos[0])
#PersonAppearance(track="1", person=people[1], video=videos[0])
#PersonAppearance(track="2", person=people[1], video=videos[1])
#PersonAppearance(track="3", person=people[2], video=videos[1])
#PersonAppearance(track="4", person=people[2], video=videos[2])
#PersonAppearance(track="5", person=people[0], video=videos[3])
#PersonAppearance(track="6", person=people[1], video=videos[3])
#PersonAppearance(track="7", person=people[2], video=videos[3])
#
#l = ("Alex", "Toy", "Dean")
#for i in xrange(len(l)):
#    print l[i]
#    print people[i].appearsIn
#
#session.commit()
