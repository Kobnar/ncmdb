__author__ = 'kobnar'
from nose.plugins.attrib import attr

from . import DBSession, SQLiteTestCase


@attr('db')
class TestPersonModel(SQLiteTestCase):

    def test_save_and_query(self):
        """Person can successfully save to and be retrieved from SQLite
        """
        actor_name = 'Nicolas Cage'
        from ..models import Person
        nic_cage = Person(name=actor_name)
        DBSession.add(nic_cage)
        DBSession.commit()
        self.assertIsInstance(nic_cage, Person)
        self.assertIsNotNone(nic_cage.id)
        self.assertEqual(nic_cage.name, actor_name)
        result = DBSession.query(Person).filter_by(name=actor_name).first()
        self.assertIsInstance(result, Person)
        self.assertIsNotNone(result.id)
        self.assertEqual(result.name, actor_name)

    def test_id_increments(self):
        """Person.id increments with each save (pure curiosity)
        """
        from ..models import Person
        actor_name_0 = 'Nicolas Cage'
        nic_cage = Person(name=actor_name_0)
        DBSession.add(nic_cage)
        DBSession.commit()
        self.assertEqual(1, nic_cage.id)
        actor_name_1 = 'Elisabeth Shue'
        beth_shue = Person(name=actor_name_1)
        DBSession.add(beth_shue)
        DBSession.commit()
        self.assertEqual(2, beth_shue.id)

    def test_name_required_index(self):
        """Person.name raises IntegrityError if it is not set
        """
        from ..models import Person
        from sqlalchemy.exc import IntegrityError
        person = Person()
        DBSession.add(person)
        with self.assertRaises(IntegrityError):
            DBSession.flush()

    def test_unique_name_index(self):
        """Person.name raises IntegrityError if a duplicate is saved to SQLite
        """
        actor_name = 'Nicolas Cage'
        from ..models import Person
        nic_cage = Person(name=actor_name)
        DBSession.add(nic_cage)
        DBSession.commit()
        nic_dupe = Person(name=actor_name)
        DBSession.add(nic_dupe)
        from sqlalchemy.exc import IntegrityError
        with self.assertRaises(IntegrityError):
            DBSession.commit()

    def test_img_uri_sets_valid_uri(self):
        """Person.image_uri sets a valid URI without raising an exception
        """
        from ..models import Person
        person = Person()
        from . import PROFILE_URIS
        from ..exceptions import ValidationError
        for uri in PROFILE_URIS:
            try:
                person.image_uri = uri
            except ValidationError:
                self.fail('Validation error raised: %s' % uri)
            self.assertEqual(uri, person.image_uri)

    def test_img_uri_field_raises_exception_with_invalid_uri(self):
        """Person.image_uri raises an exception with an invalid uri
        """
        from ..models import Person
        person = Person()
        from . import BAD_URIS
        from ..exceptions import ValidationError
        for uri in BAD_URIS:
            with self.assertRaises(ValidationError):
                person.image_uri = uri

    def test_poster_uri_sets_none_uri(self):
        """Person.image_uri does not raise an exception for 'None' values
        """
        from ..models import Person
        person = Person()
        from ..exceptions import ValidationError
        try:
            person.image_uri = None
        except ValidationError as err:
            self.fail(err.msg)

    def test_serialize_works(self):
        """Person.serialized returns a complete dict
        """
        fields = {
            'name': 'Nicolas Cage',
            'image_uri': 'https://upload.wikimedia.org/wikipedia/commons/3/33/Nicolas_Cage_2011_CC.jpg'
        }
        expected = {
            'id': None,
            'name': fields['name'],
            'image_uri': fields['image_uri'],
            'producer_credits': [],
            'director_credits': [],
            'writer_credits': [],
            'editor_credits': [],
            'cast_credits': [],
            'musician_credits': [],
        }
        from ..models import Person
        person = Person(**fields)
        self.assertEqual(expected, person.serialized)


@attr('db')
class TestFilmModel(SQLiteTestCase):

    def test_save_and_query(self):
        """Film can successfully save to and be retrieved from SQLite
        """
        film_title = 'Leaving Las Vegas'
        film_plot = 'An alcoholic Hollywood screenwriter who lost everything' \
                       'forms an uneasy relationship with a prostitute in Las' \
                       'Vegas as he endeavors to drink himself to death.'
        from ..models import Film
        leaving_lv = Film(title=film_title, plot=film_plot)
        DBSession.add(leaving_lv)
        DBSession.commit()
        self.assertIsInstance(leaving_lv, Film)
        self.assertIsNotNone(leaving_lv.id)
        self.assertEqual(film_title, leaving_lv.title)
        result = DBSession.query(Film).filter_by(title=film_title).first()
        self.assertIsInstance(result, Film)
        self.assertIsNotNone(result.id)
        self.assertEqual(film_title, result.title)

    def test_title_required_index(self):
        """Film.title raises ValidationError if not set
        """
        from ..models import Film
        from sqlalchemy.exc import IntegrityError
        film = Film()
        DBSession.add(film)
        with self.assertRaises(IntegrityError):
            DBSession.flush()

    def test_unique_title_index(self):
        """Film.title raises IntegrityError if a duplicate is saved to SQLite
        """
        film_title = 'Leaving Las Vegas'
        from ..models import Film
        leaving_lv = Film(title=film_title)
        DBSession.add(leaving_lv)
        DBSession.commit()
        leaving_lv = Film(title=film_title)
        DBSession.add(leaving_lv)
        from sqlalchemy.exc import IntegrityError
        with self.assertRaises(IntegrityError):
            DBSession.commit()

    def test_year_field(self):
        """Film.year sets a valid year
        """
        film_title = 'Leaving Las Vegas'
        from ..models import Film
        leaving_lv = Film(title=film_title, year=1995)
        DBSession.add(leaving_lv)
        DBSession.commit()
        result = DBSession.query(Film).filter_by(id=leaving_lv.id).first()
        self.assertEqual(1995, result.year)

    def test_year_field_cannot_be_negative(self):
        """Film.year raises ValidationError if the value is negative
        """
        film_title = 'Leaving Las Vegas'
        from ..models import Film
        from ..exceptions import ValidationError
        with self.assertRaises(ValidationError):
            Film(title=film_title, year=-1)

    def test_running_time_field(self):
        film_title = 'Leaving Las Vegas'
        from ..models import Film
        leaving_lv = Film(title=film_title, running_time=112)
        DBSession.add(leaving_lv)
        DBSession.commit()
        result = DBSession.query(Film).filter_by(id=leaving_lv.id).first()
        self.assertEqual(112, result.runtime)

    def test_running_time_field_cannot_be_negative(self):
        """Film.runtime raises ValidationError if the value is negative
        """
        film_title = 'Leaving Las Vegas'
        from ..models import Film
        from ..exceptions import ValidationError
        with self.assertRaises(ValidationError):
            Film(title=film_title, running_time=-1)

    def test_logline_field(self):
        film_title = 'Leaving Las Vegas'
        film_plot = 'An alcoholic Hollywood screenwriter who lost everything' \
                       'forms an uneasy relationship with a prostitute in Las' \
                       'Vegas as he endeavors to drink himself to death.'
        from ..models import Film
        leaving_lv = Film(title=film_title, plot=film_plot)
        DBSession.add(leaving_lv)
        DBSession.commit()
        result = DBSession.query(Film).filter_by(id=leaving_lv.id).first()
        self.assertEqual(film_plot, result.plot)

    def test_poster_uri_sets_valid_uri(self):
        """Film.poster_uri sets a valid URI without raising an exception
        """
        from ..models import Film
        film = Film()
        from . import POSTER_URIS
        from ..exceptions import ValidationError
        for uri in POSTER_URIS:
            try:
                film.poster_uri = uri
            except ValidationError:
                self.fail('Validation error raised: %s' % uri)
            self.assertEqual(uri, film.poster_uri)

    def test_poster_uri_field_raises_exception_with_invalid_uri(self):
        """Film.poster_uri raises an exception with an invalid URI
        """
        from ..models import Film
        film = Film()
        from . import BAD_URIS
        from ..exceptions import ValidationError
        for uri in BAD_URIS:
            with self.assertRaises(ValidationError):
                film.poster_uri = uri

    def test_poster_uri_sets_none_uri(self):
        """Film.poster_uri does not raise an exception for 'None' values
        """
        from ..models import Film
        film = Film()
        from ..exceptions import ValidationError
        try:
            film.poster_uri = None
        except ValidationError as err:
            self.fail(err.msg)

    def test_trailer_uri_sets_valid_uri(self):
        """Film.trailer_uri sets a valid URI without raising an exception
        """
        from ..models import Film
        film = Film()
        from . import TRAILER_URIS
        from ..exceptions import ValidationError
        for uri in TRAILER_URIS:
            try:
                film.trailer_uri = uri
            except ValidationError:
                self.fail('Validation error raised: %s' % uri)
            self.assertEqual(uri, film.trailer_uri)

    def test_trailer_uri_field_raises_exception_with_invalid_uri(self):
        """Film.trailer_uri raises an exception with an invalid uri
        """
        from ..models import Film
        film = Film()
        from . import BAD_URIS
        from ..exceptions import ValidationError
        for uri in BAD_URIS:
            with self.assertRaises(ValidationError):
                film.trailer_uri = uri

    def test_trailer_uri_sets_none_uri(self):
        """Film.trailer_uri does not raise an exception for 'None' values
        """
        from ..models import Film
        film = Film()
        from ..exceptions import ValidationError
        try:
            film.trailer_uri = None
        except ValidationError as err:
            self.fail(err.msg)

    def test_wiki_uri_sets_valid_uri(self):
        """Film.wiki_uri sets a valid URI without raising an exception
        """
        from ..models import Film
        film = Film()
        from . import WIKI_URIS
        from ..exceptions import ValidationError
        for uri in WIKI_URIS:
            try:
                film.wiki_uri = uri
            except ValidationError:
                self.fail('Validation error raised: %s' % uri)
            self.assertEqual(uri, film.wiki_uri)

    def test_wiki_uri_field_raises_exception_with_invalid_uri(self):
        """Film.wiki_uri raises an exception with an invalid uri
        """
        from ..models import Film
        film = Film()
        from . import BAD_URIS
        from ..exceptions import ValidationError
        for uri in BAD_URIS:
            with self.assertRaises(ValidationError):
                film.wiki_uri = uri

    def test_wiki_uri_sets_none_uri(self):
        """Film.wiki_uri does not raise an exception for 'None' values
        """
        from ..models import Film
        film = Film()
        from ..exceptions import ValidationError
        try:
            film.wiki_uri = None
        except ValidationError as err:
            self.fail(err.msg)

    def test_producers_accepts_none(self):
        """Film.producers accepts 'None' and sets an empty list
        """
        from ..models import Film
        film = Film()
        film.producers = None
        self.assertEqual([], film.producers)

    def test_directors_accepts_none(self):
        """Film.directors accepts 'None' and sets an empty list
        """
        from ..models import Film
        film = Film()
        film.directors = None
        self.assertEqual([], film.directors)

    def test_writers_accepts_none(self):
        """Film.writers accepts 'None' and sets an empty list
        """
        from ..models import Film
        film = Film()
        film.writers = None
        self.assertEqual([], film.writers)

    def test_editors_accepts_none(self):
        """Film.editors accepts 'None' and sets an empty list
        """
        from ..models import Film
        film = Film()
        film.editors = None
        self.assertEqual([], film.editors)

    def test_cast_accepts_none(self):
        """Film.cast accepts 'None' and sets an empty list
        """
        from ..models import Film
        film = Film()
        film.cast = None
        self.assertEqual([], film.cast)

    def test_musicians_accepts_none(self):
        """Film.musicians accepts 'None' and sets an empty list
        """
        from ..models import Film
        film = Film()
        film.musicians = None
        self.assertEqual([], film.musicians)

    @attr('todo')
    def test_serialize_works(self):
        fields = {
            'name': 'Nicolas Cage',
            'image_uri': 'https://upload.wikimedia.org/wikipedia/commons/3/33/Nicolas_Cage_2011_CC.jpg'
        }
        expected = {
            'id': None,
            'name': fields['name'],
            'image_uri': fields['image_uri'],
            'producer_credits': [],
            'director_credits': [],
            'writer_credits': [],
            'editor_credits': [],
            'cast_credits': [],
            'musician_credits': [],
        }
        from ..models import Person
        person = Person(**fields)
        self.assertEqual(expected, person.serialized)


@attr('db')
class TestFilmPeopleRelationships(SQLiteTestCase):

    def setUp(self):
        super(TestFilmPeopleRelationships, self).setUp()
        self.film_title = 'Leaving Las Vegas'
        self.names = ['Mike Figgis', 'Nicolas Cage', 'Elisabeth Shue']
        from ..models import Person
        self.people = [Person(name=name) for name in self.names]
        for person in self.people:
            DBSession.add(person)
        DBSession.commit()

    def test_producers_m2m_field(self):
        """Film.producers successfully populates an M2M relationship in SQLite
        """
        from ..models import Film
        leaving_lv = Film(title=self.film_title)
        leaving_lv.producers = [x for x in self.people]
        DBSession.add(leaving_lv)
        DBSession.commit()
        from ..models import Person
        for name in self.names:
            producer = DBSession.query(Person).filter_by(name=name).first()
            self.assertIn(
                self.film_title, [x.title for x in producer.producer_credits])

    def test_directors_m2m_field(self):
        """Film.directors successfully populates an M2M relationship in SQLite
        """
        from ..models import Film
        leaving_lv = Film(title=self.film_title)
        leaving_lv.directors = [x for x in self.people]
        DBSession.add(leaving_lv)
        DBSession.commit()
        from ..models import Person
        for name in self.names:
            director = DBSession.query(Person).filter_by(name=name).first()
            self.assertIn(
                self.film_title, [x.title for x in director.director_credits])

    def test_writers_m2m_field(self):
        """Film.writers successfully populates an M2M relationship in SQLite
        """
        from ..models import Film
        leaving_lv = Film(title=self.film_title)
        leaving_lv.writers = [x for x in self.people]
        DBSession.add(leaving_lv)
        DBSession.commit()
        from ..models import Person
        for name in self.names:
            writer = DBSession.query(Person).filter_by(name=name).first()
            self.assertIn(
                self.film_title, [x.title for x in writer.writer_credits])

    def test_editors_m2m_field(self):
        """Film.writers successfully populates an M2M relationship in SQLite
        """
        from ..models import Film
        leaving_lv = Film(title=self.film_title)
        leaving_lv.editors = [x for x in self.people]
        DBSession.add(leaving_lv)
        DBSession.commit()
        from ..models import Person
        for name in self.names:
            editor = DBSession.query(Person).filter_by(name=name).first()
            self.assertIn(
                self.film_title, [x.title for x in editor.editor_credits])

    def test_cast_m2m_field(self):
        """Film.cast successfully populates an M2M relationship in SQLite
        """
        from ..models import Film
        leaving_lv = Film(title=self.film_title)
        leaving_lv.cast = [x for x in self.people]
        DBSession.add(leaving_lv)
        DBSession.commit()
        from ..models import Person
        for name in self.names:
            cast = DBSession.query(Person).filter_by(name=name).first()
            self.assertIn(
                self.film_title, [x.title for x in cast.cast_credits])

    @attr('todo')
    def test_cast_m2m_role(self):
        """Film.cast successfully adds relational metadata of "role"
        """
        self.fail()

    def test_musicians_m2m_field(self):
        """Film.musicians successfully populates an M2M relationship in SQLite
        """
        from ..models import Film
        leaving_lv = Film(title=self.film_title)
        leaving_lv.musicians = [x for x in self.people]
        DBSession.add(leaving_lv)
        DBSession.commit()
        from ..models import Person
        for name in self.names:
            musicians = DBSession.query(Person).filter_by(name=name).first()
            self.assertIn(
                self.film_title, [x.title for x in musicians.musician_credits])

    @attr('todo')
    def test_cinematographers(self):
        """Film.cinematographers successfully populates an M2M relationship in SQLite
        """
        self.fail()

    @attr('todo')
    def test_credits_with_links(self):
        """Person.serialized should return a list of titles for credits, not objects
        """
        self.fail()