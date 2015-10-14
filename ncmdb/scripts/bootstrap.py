__author__ = 'kobnar'

import re
import json
import os
from shutil import copyfile
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from ..models import Base, Person, Film
from ..resources import FilmTableResource, PersonTableResource


class BaseManager(object):

    SESSION = scoped_session(sessionmaker())
    ENGINE = create_engine('sqlite:///ncmdb/ncmdb.sqlite')
    SESSION.configure(bind=ENGINE)


class NCMDBManager(BaseManager):
    """
    A class designed to bootstrap NCMDB data.
    """

    DATA_PATH = 'ncmdb/scripts/ncmdb.json'

    def __init__(self):
        self.people = set()

    def backup(self):
        if os.path.exists(self.DATA_PATH):
            backup_path = self.DATA_PATH + '_BACKUP'
            copyfile(self.DATA_PATH, backup_path)

    def reset(self):
        print('Dropping old tables from existing database...')
        Base.metadata.drop_all(self.ENGINE)
        print('Creating new tables in database...')
        Base.metadata.create_all(self.ENGINE)

    def save(self, make_backup=True):
        """
        Serializes the current NCMDB into a monolithic JSON file.
        """
        if make_backup:
            self.backup()
        os.remove(self.DATA_PATH)

        print('Serializing films...')
        films = FilmTableResource(None, 'films', self.SESSION).retrieve()
        film_data = [f.serialize(False) for f in films]

        print('Serializing people...')
        people = PersonTableResource(None, 'people', self.SESSION).retrieve()
        people_data = [p.serialize(False) for p in people]

        ncmdb_data = {
            'films': film_data,
            'people': people_data,
        }

        print('Saving data...')
        with open(self.DATA_PATH, 'w') as ncmdb_file:
            json.dump(ncmdb_data, ncmdb_file,
                      indent=4, separators=(', ', ': '))

    def load(self):
        """
        Wipes the existing database and deserializes the backup JSON file.
        """

        def _link_person(film, field, names):
            if names:
                for name in names:
                    q_prs = self.SESSION.query(Person).\
                        filter_by(name=name).first()
                    getattr(film, field).append(q_prs)
            else:
                setattr(film, field, [])

        self.reset()
        print('Opening data...')
        with open(self.DATA_PATH) as ncmdb_file:
            ncmdb_data = json.load(ncmdb_file)
            print('Deserializing people...')
            for person_data in ncmdb_data['people']:
                print('\t{}'.format(person_data['name']))
                person = Person()
                person.name = person_data['name']
                person.image_uri = person_data['image_uri']
                self.SESSION.add(person)
                self.people.add(person_data['name'])
            self.SESSION.commit()
            print('Deserializing films...')
            for film_data in ncmdb_data['films']:
                print('\t{}'.format(film_data['title']))
                film = Film()
                film.title = film_data['title']
                film.plot = film_data['plot']
                film.rating = film_data['rating']
                film.year = film_data['year']
                film.runtime = film_data['runtime']
                film.poster_uri = film_data['poster_uri']
                film.trailer_uri = film_data['trailer_uri']
                film.wiki_uri = film_data['wiki_uri']
                _link_person(film, 'producers', film_data['producers'])
                _link_person(film, 'directors', film_data['directors'])
                _link_person(film, 'writers', film_data['writers'])
                _link_person(film, 'editors', film_data['editors'])
                _link_person(film, 'cast', film_data['cast'])
                _link_person(film, 'musicians', film_data['musicians'])
            self.SESSION.commit()
        print('Fetching images...')
        for film in self.SESSION.query(Film):
            print('\tFetching {}'.format(film.poster_uri))
            film.fetch_poster()
        self.SESSION.commit()


class OMDBManager(BaseManager):
    """
    A class designed to bootstrap NCMDB data using external sources.
    """

    DATA_PATH = 'ncmdb/scripts/sources/omdb.json',

    ACCEPTED_CREDITS = (
        None,
        'story',
        'screen story',
        'screenplay',
    )

    # def __init__(self):




# def serialize_omdb_int(int_str):
#     if int_str:
#         if int_str.endswith(' min'):
#             int_str = int_str[:-4]
#         return int(int_str)
#
#
# def parse_credit(credit):
#     """
#     Takes a credit string and splits it into a name and a note.
#
#     :param credit: A credit string (e.g. 'John Nickle (book)')
#     :return: A name/credit pair (e.g. ['john Nickle', 'book'])
#     """
#     note_pattern = re.compile('^(.+?)(?: \((.+)\))?$')
#     result = note_pattern.search(credit).groups()
#     if len(result) == 1:
#         return result[0], None
#     else:
#         return result[0], result[1]
#
#
# def serialize_omdb_people(credit):
#     """
#     Parses a comma delineated string of peoples' names, instantiates each name
#     into a proper NCMDB Person object, and saves each object to the database
#     if it does not already exist.
#
#     :param credit: A comma delineated list of people
#     :return: A Python list of database IDs for each person
#     """
#     if credit:
#         credit_list = credit.split(', ')
#         name_list = [parse_credit(credit) for credit in credit_list]
#         name_list = [name for name, credit in name_list
#                      if credit in ALLOWED_CREDITS]
#         people = []
#         for name in name_list:
#             person = DBSession.query(Person).filter_by(name=name).first()
#             if not person:
#                 print('\t\t\'{}\''.format(name))
#                 person = Person(name=name)
#                 DBSession.add(person)
#             people.append(person)
#         DBSession.commit()
#         return people
#
#
# def serialize_omdb_film(film_data):
#     """
#     Translates an Open Movie Database JSON object into a proper NCMDB Film
#     object and saves the newly creates film to the Database.
#     """
#     print('\t\'{}\''.format(film_data['Title']))
#     for key, value in film_data.items():
#         if value == 'N/A':
#             film_data[key] = None
#     film = Film()
#     film.title = film_data['Title']
#     film.plot = film_data['Plot']
#     film.year = serialize_omdb_int(film_data['Year'])
#     film.rating = film_data['Rated']
#     film.runtime = serialize_omdb_int(film_data['Runtime'])
#     film.directors = serialize_omdb_people(film_data['Director'])
#     film.writers = serialize_omdb_people(film_data['Writer'])
#     film.cast = serialize_omdb_people(film_data['Actors'])
#     film.poster_uri = film_data['Poster']
#     DBSession.add(film)
#     DBSession.commit()
#     return film
#
#
# class OMDBManager(object):
#     """
#     Tasked with de-serializing Open Movie Databse data.
#     """
#
#     DATA_PATH = 'ncmdb/scripts/sources/omdb.json',
#
#     ALLOWED_CREDITS = (
#         None,
#         'story',
#         'screen story',
#         'screenplay',
#     )





# def load_omdb():
#     reset()
#     print('Serializing OMDB data...')
#     with open(DATA_PATHS['omdb']) as omdb_file:
#         omdb_data = json.load(omdb_file)
#         for film in omdb_data:
#             serialize_omdb_film(film)

