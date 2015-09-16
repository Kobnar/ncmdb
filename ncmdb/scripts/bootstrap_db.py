__author__ = 'kobnar'

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from ..models import Base, Person, Film


DBSession = scoped_session(sessionmaker())
engine = create_engine('sqlite:///ncmdb/ncmdb.sqlite')
DBSession.configure(bind=engine)
Base.metadata.create_all(engine)


PEOPLE = [
    {
        'name': 'Nicolas Cage',
        'img_uri': 'https://upload.wikimedia.org/wikipedia/commons/3/33/Nicolas_Cage_2011_CC.jpg',
    },
    {
        'name': 'Bernadette Colognne',
        'img_uri': '',
    },
    {
        'name': 'Crispin Glover',
        'img_uri': '',
    },
    {
        'name': 'Jackie Mason',
        'img_uri': '',
    },
    {
        'name': 'Julie Piekarski',
        'img_uri': '',
    },
    {
        'name': 'Jill Schoelen',
        'img_uri': '',
    },
    {
        'name': 'Mitch Guy',
        'img_uri': '',
    },
    {
        'name': 'Don Mischer',
        'img_uri': '',
    },
    {
        'name': 'George Schlatter',
        'img_uri': '',
    },
    {
        'name': 'Bob Arnott',
        'img_uri': '',
    },
    {
        'name': 'Carol Hatfield Sarasohn',
        'img_uri': '',
    },
    {
        'name': 'Lane Sarasohn',
        'img_uri': '',
    },
    {
        'name': 'Michael Warren',
        'img_uri': '',
    },
    {
        'name': 'Ken Morrisey',
        'img_uri': '',
    },
    {
        'name': 'Amy Heckerling',
        'img_uri': '',
    },
    {
        'name': 'Irving Azoff',
        'img_uri': '',
    },
    {
        'name': 'Cameron Crowe',
        'img_uri': '',
    },
    {
        'name': 'Sean Penn',
        'img_uri': '',
    },
    {
        'name': 'Jennifer Jason Leigh',
        'img_uri': '',
    },
    {
        'name': 'Judge Reinhold',
        'img_uri': '',
    },
    {
        'name': 'Phoebe Cates',
        'img_uri': '',
    },
    {
        'name': 'Brian Backer',
        'img_uri': '',
    },
    {
        'name': 'Robert Romanus',
        'img_uri': '',
    },
    {
        'name': 'Ray Walston',
        'img_uri': '',
    },
    {
        'name': 'Matthew F. Leonetti',
        'img_uri': '',
    },
    {
        'name': 'Eric Jenkins',
        'img_uri': '',
    },
    {
        'name': 'Art Linson',
        'img_uri': '',
    },
    {
        'name': 'Andrew Lane',
        'img_uri': '',
    },
    {
        'name': 'Wayne Crawford',
        'img_uri': '',
    },
    {
        'name': 'Éva Gárdos',
        'img_uri': '',
    },
    {
        'name': 'Elizabeth Daily',
        'img_uri': '',
    },
    {
        'name': 'Frederic Forrest',
        'img_uri': '',
    },
    {
        'name': 'Richard Sanders',
        'img_uri': '',
    },
    {
        'name': 'Colleen Camp',
        'img_uri': '',
    },
    {
        'name': 'Deborah Foreman',
        'img_uri': '',
    },
    {
        'name': 'Lee Purcell',
        'img_uri': '',
    },
    {
        'name': 'Cameron Dye',
        'img_uri': '',
    },
    {
        'name': 'Michelle Meyrink',
        'img_uri': '',
    },
    {
        'name': 'Diana Scarwid',
        'img_uri': '',
    },
    {
        'name': 'Diane Lane',
        'img_uri': '',
    },
    {
        'name': 'Dennis Hopper',
        'img_uri': '',
    },
    {
        'name': 'Vincent Spano',
        'img_uri': '',
    },
    {
        'name': 'Matt Dillon',
        'img_uri': '',
    },
    {
        'name': 'Mickey Rourke',
        'img_uri': '',
    },
    {
        'name': 'Fred Roos',
        'img_uri': '',
    },
    {
        'name': 'Francis Ford Coppola',
        'img_uri': '',
    },
    {
        'name': 'Doug Claybourne',
        'img_uri': '',
    },
    {
        'name': 'Barry Malkin',
        'img_uri': '',
    },
    {
        'name': 'S. E. Hinton',
        'img_uri': '',
    },
    {
        'name': 'Elizabeth McGovern',
        'img_uri': '',
    },
    {
        'name': 'Alain Bernheim',
        'img_uri': '',
    },
    {
        'name': 'John Kohn',
        'img_uri': '',
    },
    {
        'name': 'Steven Kloves',
        'img_uri': '',
    },
    # {
    #     'name': '',
    #     'img_uri': '',
    # },
]


FILMS = [
    {
        'title': 'Best of Times',
        'year': 1981,
        'running_time': 48,
        'description': 'Best of Times is a 1981 television pilot episode'
                       'directed by Don Mischer, intended to be the for a'
                       'series that never got picked up. It is also the acting'
                       'debut of Crispin Glover and Nicolas Cage.',
        'poster_uri': '',
        'trailer_uri': '',
        'wiki_uri': 'https://en.wikipedia.org/wiki/Best_of_Times_(1981_film)',
        'producers': ['Don Mischer', 'George Schlatter'],
        'directors': ['Don Mischer'],
        'writers': ['Bob Arnott', 'Carol Hatfield Sarasohn', 'Lane Sarasohn'],
        'editors': ['Ken Morrisey'],
        'cast': ['Crispin Glover', 'Nicolas Cage'],
        'musicians': ['Michael Warren'],
    },
    {
        'title': 'Fast Times at Ridgemont High',
        'year': 1982,
        'running_time': 90,
        'description': '',
        'poster_uri': '',
        'trailer_uri': '',
        'wiki_uri': 'https://en.wikipedia.org/wiki/Fast_Times_at_Ridgemont_High',
        'producers': ['Irving Azoff', 'Art Linson'],
        'directors': ['Amy Heckerling'],
        'writers': ['Cameron Crowe'],
        'editors': ['Eric Jenkins'],
        'cast': ['Sean Penn', 'Jennifer Jason Leigh', 'Judge Reinhold',
                 'Phoebe Cates', 'Brian Backer', 'Robert Romanus',
                 'Ray Walston', 'Nicolas Cage'],
        'musicians': [''],
    },
    {
        'title': 'Valley Girl',
        'year': 1983,
        'running_time': 99,
        'description': '',
        'poster_uri': '',
        'trailer_uri': '',
        'wiki_uri': '',
        'producers': ['Wayne Crawford', 'Andrew Lane'],
        'directors': ['Martha Coolidge'],
        'writers': ['Wayne Crawford', 'Andrew Lane'],
        'editors': ['Éva Gárdos'],
        'cast': ['Nicolas Cage', 'Deborah Foreman', 'Elizabeth Daily',
                 'Cameron Dye', 'Michelle Meyrink', 'Lee Purcell',
                 'Richard Sanders', 'Colleen Camp', 'Frederic Forrest'],
        'musicians': ['Richard Butler', 'The Plimsouls',  'The Payolas',
                      'Peter Case',  'Josie Cotton',  'Scott Wilk'],
    },
    {
        'title': 'Rumble Fish',
        'year': 1983,
        'running_time': 94,
        'description': '',
        'poster_uri': '',
        'trailer_uri': '',
        'wiki_uri': 'https://en.wikipedia.org/wiki/Rumble_Fish',
        'producers': ['Francis Ford Coppola', 'Doug Claybourne', 'Fred Roos'],
        'directors': ['Francis Ford Coppola'],
        'writers': ['S. E. Hinton', 'Francis Ford Coppola'],
        'editors': ['Barry Malkin'],
        'cast': ['Matt Dillon', 'Mickey Rourke', 'Vincent Spano',
                 'Diane Lane', 'Diana Scarwid', 'Nicolas Cage',
                 'Dennis Hopper'],
        'musicians': ['Stewart Copeland'],
    },
    {
        'title': 'Racing with the Moon',
        'year': 1984,
        'running_time': 108,
        'description': '',
        'poster_uri': '',
        'trailer_uri': '',
        'wiki_uri': 'https://en.wikipedia.org/wiki/Racing_with_the_Moon',
        'producers': ['Alain Bernheim', 'John Kohn'],
        'directors': ['Richard Benjamin'],
        'writers': ['Steven Kloves'],
        'editors': [''],
        'cast': ['Sean Penn', 'Elizabeth McGovern', 'Nicolas Cage'],
        'musicians': ['Dave Grusin'],
    },
    # {
    #     'title': '',
    #     'year': 0,
    #     'running_time': 0,
    #     'description': '',
    #     'poster_uri': '',
    #     'trailer_uri': '',
    #     'wiki_uri': '',
    #     'producers': [''],
    #     'directors': [''],
    #     'writers': [''],
    #     'editors': [''],
    #     'cast': [''],
    #     'musicians': [''],
    # },
]


def bootstrap_people():
    """
    Deserializes people and saves them to the database.
    """
    for person in PEOPLE:
        print('Creating person: \'{}\'.'.format(person['name']))
        person_obj = Person(name=person['name'], img_uri=person['img_uri'])
        DBSession.add(person_obj)
    print('Saving new people.')
    DBSession.commit()


def bootstrap_db():
    Base.metadata.drop_all(engine)
    bootstrap_people()
