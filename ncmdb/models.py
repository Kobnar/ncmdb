from sqlalchemy import Table, Column, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from zope.sqlalchemy import ZopeTransactionExtension

from .exceptions import ValidationError


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


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
    Column('actor', Integer, ForeignKey('person.id')),
    Column('role', Text))


musician_credit = Table(
    'musician_credit', Base.metadata,
    Column('film', Integer, ForeignKey('film.id')),
    Column('writer', Integer, ForeignKey('person.id')))


class Person(Base):
    """
    A person who has worked as a director, writer or actor on a film.
    """

    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    img_uri = Column(Text)


class Film(Base):
    """
    A feature film.
    """

    __tablename__ = 'film'

    id = Column(Integer, primary_key=True)

    # Local data:
    _title = Column(Text, unique=True)
    _year = Column(Integer)
    _running_time = Column(Integer)
    description = Column(Text)

    # Remote data:
    _poster_uri = Column(Text)
    _trailer_uri = Column(Text)
    _wiki_uri = Column(Text)

    # FK relationships:
    producers = relationship(
        'Person', secondary=producer_credit, backref='producer_credits')
    directors = relationship(
        'Person', secondary=director_credit, backref='director_credits')
    writers = relationship(
        'Person', secondary=writer_credit, backref='writer_credits')
    editors = relationship(
        'Person', secondary=editor_credit, backref='editor_credits')
    cast = relationship(
        'Person', secondary=cast_credit, backref='cast_credits')
    musicians = relationship(
        'Person', secondary=musician_credit, backref='musician_credits')

    @hybrid_property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if not title:
            raise ValidationError('title', title)
        self._title = title

    @hybrid_property
    def year(self):
        return self._year

    @year.setter
    def year(self, year):
        if year < 0:
            raise ValidationError('year', year)
        self._year = year

    @hybrid_property
    def running_time(self):
        return self._running_time

    @running_time.setter
    def running_time(self, running_time):
        if running_time < 0:
            raise ValidationError('running_time', running_time)
        self._running_time = running_time
