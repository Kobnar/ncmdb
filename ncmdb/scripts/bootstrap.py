__author__ = 'kobnar'

import re
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from ..models import Base, Person, Film


DBSession = scoped_session(sessionmaker())
engine = create_engine('sqlite:///ncmdb/ncmdb.sqlite')
DBSession.configure(bind=engine)


DATA_PATHS = {
    'omdb': 'ncmdb/scripts/sources/omdb.json',
    'wiki': 'ncmdb/scripts/sources/wiki.csv'
}


ALLOWED_CREDITS = (
    None,
    'story',
    'screen story',
    'screenplay',
)


def serialize_omdb_int(int_str):
    if int_str:
        if int_str.endswith(' min'):
            int_str = int_str[:-4]
        return int(int_str)


def parse_credit(credit):
    """
    Takes a credit string and splits it into a name and a note.

    :param credit: A credit string (e.g. 'John Nickle (book)')
    :return: A name/credit pair (e.g. ['john Nickle', 'book'])
    """
    note_pattern = re.compile('^(.+?)(?: \((.+)\))?$')
    result = note_pattern.search(credit).groups()
    if len(result) == 1:
        return result[0], None
    else:
        return result[0], result[1]


def serialize_omdb_people(credit):
    """
    Parses a comma delineated string of peoples' names, instantiates each name
    into a proper NCMDB Person object, and saves each object to the database
    if it does not already exist.

    :param credit: A comma delineated list of people
    :return: A Python list of database IDs for each person
    """
    if credit:
        credit_list = credit.split(', ')
        name_list = [parse_credit(credit) for credit in credit_list]
        name_list = [name for name, credit in name_list
                     if credit in ALLOWED_CREDITS]
        people = []
        for name in name_list:
            person = DBSession.query(Person).filter_by(name=name).first()
            if not person:
                print('\t\t\'{}\''.format(name))
                person = Person(name=name)
                DBSession.add(person)
            people.append(person)
        DBSession.commit()
        return people


def serialize_omdb_film(film_data):
    """
    Translates an Open Movie Database JSON object into a proper NCMDB Film
    object and saves the newly creates film to the Database.
    """
    print('\t\'{}\''.format(film_data['Title']))
    for key, value in film_data.items():
        if value == 'N/A':
            film_data[key] = None
    film = Film()
    film.title = film_data['Title']
    film.plot = film_data['Plot']
    film.year = serialize_omdb_int(film_data['Year'])
    film.rating = film_data['Rated']
    film.running_time = serialize_omdb_int(film_data['Runtime'])
    film.directors = serialize_omdb_people(film_data['Director'])
    film.writers = serialize_omdb_people(film_data['Writer'])
    film.cast = serialize_omdb_people(film_data['Actors'])
    film.poster_uri = film_data['Poster']
    DBSession.add(film)
    DBSession.commit()
    return film


def _serialize_omdb():
    """
    Serializes each film in the OMDB JSON data file into a proper NCMDB object
    and saves each new object to the database as a row.
    """
    with open(DATA_PATHS['omdb']) as omdb_file:
        omdb_data = json.load(omdb_file)
        for film in omdb_data:
            serialize_omdb_film(film)


def bootstrap():
    print('Dropping old tables from existing database...')
    Base.metadata.drop_all(engine)
    print('Creating new tables in database...')
    Base.metadata.create_all(engine)
    print('Serializing OMDB data...')
    _serialize_omdb()
