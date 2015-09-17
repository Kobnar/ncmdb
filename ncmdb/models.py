from sqlalchemy import Table, Column, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from zope.sqlalchemy import ZopeTransactionExtension

from .exceptions import ValidationError
from .validators import validate_uri


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
    A person who has had the fortunate glory of working in the presence of our
    Lord, Nicolas Coppola, or bears a credit of note on a project He hath
    Caged with but a fraction of His unending might.
    """

    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    _img_uri = Column(Text)

    @hybrid_property
    def img_uri(self):
        """
        A URI pointing to a remote profile image for this person.
        """
        return self._img_uri

    @img_uri.setter
    def img_uri(self, uri):
        if not validate_uri(uri):
            raise ValidationError('poster_uri', uri)
        self._img_uri = uri

    @property
    def serialized(self):
        """
        A dictionary-serialized version of the data for this person (for use
        with a JSON renderer, etc.).
        """
        return {
            'id': self.id,
            'name': self.name,
            'img_uri': self.img_uri,
            'producer_credits': self.producer_credits,
            'director_credits': self.director_credits,
            'writer_credits': self.writer_credits,
            'editor_credits': self.editor_credits,
            'cast_credits': self.cast_credits,
            'musician_credits': self.musician_credits
        }


class Film(Base):
    """
    A film featuring the magnificent Nicolas Cage, may his light shine upon
    this web app with gracious indifference or aplomb, and his name echo into
    the skies as though a thousand horns hath spake his name.
    """

    __tablename__ = 'film'

    id = Column(Integer, primary_key=True)

    # Local data:
    title = Column(Text, unique=True, nullable=False)
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
    def year(self):
        """
        The year this film was first released.
        """
        return self._year

    @year.setter
    def year(self, year):
        if year < 0:
            raise ValidationError('year', year)
        self._year = year

    @hybrid_property
    def running_time(self):
        """
        The total running time of this film (in minutes).
        """
        return self._running_time

    @running_time.setter
    def running_time(self, running_time):
        if running_time < 0:
            raise ValidationError('running_time', running_time)
        self._running_time = running_time

    @hybrid_property
    def poster_uri(self):
        """
        A URI pointing to a remote poster image for this film.
        """
        return self._poster_uri

    @poster_uri.setter
    def poster_uri(self, uri):
        if not validate_uri(uri):
            raise ValidationError('poster_uri', uri)
        self._poster_uri = uri

    @hybrid_property
    def trailer_uri(self):
        """
        A URI pointing to a remote trailer for this film.
        """
        return self._trailer_uri

    @trailer_uri.setter
    def trailer_uri(self, uri):
        if not validate_uri(uri):
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
        if not validate_uri(uri):
            raise ValidationError('wiki_uri', uri)
        self._wiki_uri = uri

    @property
    def serialized(self):
        """
        A dictionary-serialized version of the data for this film (for use with
        a JSON renderer, etc.).
        """
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'running_time': self.running_time,
            'producers': [p.name for p in self.producers],
            'directors': [d.name for d in self.directors],
            'writers': [w.name for w in self.writers],
            'editors': [e.name for e in self.editors],
            'cast': [c.name for c in self.editors],
            'musicians': [m.name for m in self.musicians]
        }
