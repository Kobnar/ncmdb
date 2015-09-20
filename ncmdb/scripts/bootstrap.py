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
        self.films = set()
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
                person.img_uri = person_data['img_uri']
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
