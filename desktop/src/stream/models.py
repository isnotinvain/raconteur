from elixir import *

class Person(Entity):
    name = Field(Text(), primary_key=True)
    appearsIn = ManyToMany('Video')

    def __repr__(self):
        return '<Person: "%s">' % (self.name)

class Video(Entity):
    path = Field(Text())
    creation = Field(Integer())
    containsPeople = ManyToMany('Person')

    def __repr__(self):
        return '<Video: "%s">' % (self.path)
