__author__ = 'kobnar'

from unittest import TestCase
from sqlalchemy.orm import scoped_session, sessionmaker

from ..models import Base


DBSession = scoped_session(sessionmaker())


class SQLiteTestCase(TestCase):
    def setUp(self):
        from sqlalchemy import create_engine
        engine = create_engine('sqlite:///:memory:')
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)

    def tearDown(self):
        DBSession.remove()


GOOD_URIS = [
    'https://upload.wikimedia.org/wikipedia/commons/3/33/Nicolas_Cage_2011_CC.jpg',
    'https://upload.wikimedia.org/wikipedia/commons/c/c0/Nicolas_Cage_Deauville_2013.jpg',
    'https://upload.wikimedia.org/wikipedia/en/7/7f/Fast_Times_at_Ridgemont_High_film_poster.jpg',
    'https://upload.wikimedia.org/wikipedia/en/f/fa/Outsidersposter.jpeg',
    'https://upload.wikimedia.org/wikipedia/en/f/f7/Bringing_out_the_dead.jpg',
    'https://upload.wikimedia.org/wikipedia/en/8/8e/Matchstick_Men.jpg',
    'https://upload.wikimedia.org/wikipedia/en/5/5e/Adaptation._film.jpg',
    'https://upload.wikimedia.org/wikipedia/en/f/f1/Mandolinfilm1.jpg',
    'https://upload.wikimedia.org/wikipedia/en/f/fa/Wicker-man-poster.jpg',
    ]

# TODO: Create a better collection of bad URIs.
BAD_URIS = [
    'nodomain',
    'g^gl.X',
    ]
