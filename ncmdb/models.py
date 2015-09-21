__author__ = 'kobnar'

import os
import re
from urllib.request import urlretrieve
from sqlalchemy import Table, Column, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from zope.sqlalchemy import ZopeTransactionExtension

from .exceptions import ValidationError
from .validators import validate_uri


# Used for image caching:
_CACHE_PATH = 'ncmdb/static/img/cache/'
_IMG_REGEX = re.compile('([^/]+\.jpg)$')


# SQLAlchemy session management:
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


# M2M relationships:

producer_credit = Table(
    'producer_credit', Base.metadata,
    Column('film', Integer, ForeignKey('film.id')),
    Column('producer', Integer, ForeignKey('person.id')))


director_credit = Table(
    'director_credit', Base.metadata,
    Column('film', Integer, ForeignKey('film.id')),
    Column('director', Integer, ForeignKey('person.id')))


writer_credit = Table(
    'writer_credit', Base.metadata,
    Column('film', Integer, ForeignKey('film.id')),
    Column('writer', Integer, ForeignKey('person.id')))


editor_credit = Table(
    'editor_credit', Base.metadata,
    Column('film', Integer, ForeignKey('film.id')),
    Column('writer', Integer, ForeignKey('person.id')))


cast_credit = Table(
    'cast_credit', Base.metadata,
    Column('film', Integer, ForeignKey('film.id')),
    Column('actor', Integer, ForeignKey('person.id')))


musician_credit = Table(
    'musician_credit', Base.metadata,
    Column('film', Integer, ForeignKey('film.id')),
    Column('writer', Integer, ForeignKey('person.id')))


# SQL Tables:

class Person(Base):
    """
    A person who has had the fortunate glory of working in the presence of our
    Lord, Nicolas Coppola, or bears a credit of note on a project He hath
    Caged with but a fraction of His unending might.
    """

    __tablename__ = 'person'

    FIELD_CHOICES = [
        'name',
        'image_uri',
        'image_cache',
        'producer_credits',
        'director_credits',
        'writer_credits',
        'editor_credits',
        'cast_credits',
        'musician_credits',
    ]

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    _image_uri = Column(Text)
    _image_cache = Column(Text)

    @hybrid_property
    def image_uri(self):
        """
        A URI pointing to a remote profile image for this person.
        """
        return self._image_uri

    @image_uri.setter
    def image_uri(self, uri):
        if uri and not validate_uri(uri):
            raise ValidationError('poster_uri', uri)
        self._image_uri = uri

    def fetch_image(self):
        """
        A method designed to create a local cache of this person's profile
        image.
        """
        if self._image_cache:
            file_name = '{}.jpg'.format(self.id)
            os.makedirs(self.CACHE_PATH, exist_ok=True)
            urlretrieve(self.image_uri, self.CACHE_PATH + file_name)
            self._image_cache = file_name
            return self._image_cache

    @hybrid_property
    def image_cache(self):
        """
        A URI pointing to the locale cache of the poster_cache for this film.

        NOTE: If no local cache exists, this property automatically calls
        `Film.fetch_poster()` to create one.
        """
        if not self._image_cache:
            self.fetch_image()
        return self._image_cache

    @staticmethod
    def _serialize_field(field, value, trim):
        output = {}
        if value:
            if type(value) is not int and type(value[0]) is Film:
                output[field] = [x.title for x in value]
            else:
                output[field] = value
        elif not trim:
            output[field] = None
        return output

    def serialize(self, trim=True):
        """
        A custom JSON serializing method.
        """
        output = {
            'id': self.id,
            'name': self.name
        }
        for key in self.FIELD_CHOICES:
            value = getattr(self, key)
            output.update(self._serialize_field(key, value, trim))
        return output

    def __json__(self, request):
        return self.serialize()


class Film(Base):
    """
    A film featuring the magnificent Nicolas Cage, may his light shine upon
    this web app with gracious indifference or aplomb, and his name echo into
    the skies as though a thousand horns hath spake his name.
    """

    __tablename__ = 'film'

    CACHE_PATH = _CACHE_PATH + 'posters/'

    FIELD_CHOICES = [
        'title',
        'plot',
        'rating',
        'year',
        'runtime',
        'producers',
        'directors',
        'writers',
        'editors',
        'cast',
        'musicians',
        'poster_uri',
        'poster_cache',
        'trailer_uri',
        'wiki_uri',
    ]

    id = Column(Integer, primary_key=True)

    # Local data:
    title = Column(Text, unique=True, nullable=False)
    plot = Column(Text)
    rating = Column(Text)
    _year = Column(Integer)
    _runtime = Column(Integer)
    _poster_cache = Column(Text)

    # Remote data:
    _poster_uri = Column(Text)
    _trailer_uri = Column(Text)
    _wiki_uri = Column(Text)

    # FK relationships:
    _producers = relationship(
        'Person', secondary=producer_credit, backref='producer_credits')
    _directors = relationship(
        'Person', secondary=director_credit, backref='director_credits')
    _writers = relationship(
        'Person', secondary=writer_credit, backref='writer_credits')
    _editors = relationship(
        'Person', secondary=editor_credit, backref='editor_credits')
    _cast = relationship(
        'Person', secondary=cast_credit, backref='cast_credits')
    _musicians = relationship(
        'Person', secondary=musician_credit, backref='musician_credits')

    @hybrid_property
    def year(self):
        """
        The year this film was first released.
        """
        return self._year

    @year.setter
    def year(self, year):
        if year and year < 0:
            raise ValidationError('year', year)
        self._year = year

    @hybrid_property
    def runtime(self):
        """
        The total running time of this film (in minutes).
        """
        return self._runtime

    @runtime.setter
    def runtime(self, running_time):
        if running_time and running_time < 0:
            raise ValidationError('runtime', running_time)
        self._runtime = running_time

    @hybrid_property
    def producers(self):
        return self._producers

    @producers.setter
    def producers(self, list):
        if not list:
            list = []
        self._producers = list

    @hybrid_property
    def directors(self):
        return self._directors

    @directors.setter
    def directors(self, list):
        if not list:
            list = []
        self._directors = list

    @hybrid_property
    def writers(self):
        return self._writers

    @writers.setter
    def writers(self, list):
        if not list:
            list = []
        self._writers = list

    @hybrid_property
    def editors(self):
        return self._editors

    @editors.setter
    def editors(self, list):
        if not list:
            list = []
        self._editors = list

    @hybrid_property
    def cast(self):
        return self._cast

    @cast.setter
    def cast(self, list):
        if not list:
            list = []
        self._cast = list

    @hybrid_property
    def musicians(self):
        return self._musicians

    @musicians.setter
    def musicians(self, list):
        if not list:
            list = []
        self._musicians = list


    @hybrid_property
    def poster_uri(self):
        """
        A URI pointing to a remote poster_cache image for this film.
        """
        return self._poster_uri

    @poster_uri.setter
    def poster_uri(self, uri):
        if uri and not validate_uri(uri):
            raise ValidationError('poster_uri', uri)
        self._poster_uri = uri

    def fetch_poster(self):
        """
        A method designed to fetch a poster_cache image based on the URI provided in
        `Film.poster_uri`.
        """
        if self._poster_uri:
            file_name = '{}.jpg'.format(self.id)
            os.makedirs(self.CACHE_PATH, exist_ok=True)
            urlretrieve(self.poster_uri, self.CACHE_PATH + file_name)
            self._poster_cache = file_name
            return self._poster_cache

    @hybrid_property
    def poster_cache(self):
        """
        A URI pointing to the locale cache of the poster_cache for this film.

        NOTE: If no local cache exists, this property automatically calls
        `Film.fetch_poster()` to create one.
        """
        if not self._poster_cache:
            self.fetch_poster()
        return self._poster_cache

    @hybrid_property
    def trailer_uri(self):
        """
        A URI pointing to a remote trailer for this film.
        """
        return self._trailer_uri

    @trailer_uri.setter
    def trailer_uri(self, uri):
        if uri and not validate_uri(uri):
            raise ValidationError('trailer_uri', uri)
        self._trailer_uri = uri

    @hybrid_property
    def wiki_uri(self):
        """
        A URI pointing to a remote wiki page for this film.
        """
        return self._wiki_uri

    @wiki_uri.setter
    def wiki_uri(self, uri):
        if uri and not validate_uri(uri):
            raise ValidationError('wiki_uri', uri)
        self._wiki_uri = uri

    @staticmethod
    def _serialize_field(field, value, trim):
        output = {}
        if value:
            if type(value) is not int and type(value[0]) is Person:
                output[field] = [x.name for x in value]
            else:
                output[field] = value
        elif not trim:
            output[field] = None
        return output

    def serialize(self, trim=True):
        """
        A custom JSON serializing method.
        """
        output = {
            'id': self.id,
            'title': self.title
        }
        for key in self.FIELD_CHOICES:
            value = getattr(self, key)
            output.update(self._serialize_field(key, value, trim))
        return output

    def __json__(self, request):
        return self.serialize()
