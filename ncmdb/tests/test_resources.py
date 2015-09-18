__author__ = 'kobnar'
from nose.plugins.attrib import attr

from . import DBSession, SQLiteTestCase


class PersonResourceTestCase(SQLiteTestCase):
    """
    A test case for PersonTableResource and PersonRowResource test suites.
    """
    def setUp(self):
        super(PersonResourceTestCase, self).setUp()
        from ..resources import PersonTableResource
        self.table_resource = PersonTableResource(None, 'people', DBSession)
        self.people = []
        from . import PEOPLE
        from ..models import Person
        for name in PEOPLE:
            person = Person(name=name)
            self.people.append(person)
            DBSession.add(person)
        DBSession.commit()


class PersonRowResourceTests(PersonResourceTestCase):
    """
    Integration tests for :class:`resources.PersonRowResource` (effectively
    covers all test cases for :class:`resources.RowResource`).
    """

    def test_retrieve_works(self):
        """PersonRowResource.retrieve() returns the correct Person for all entities
        """
        from ..models import Person
        for idx, person in enumerate(self.people):
            expected = self.people[idx]
            row_resource = self.table_resource[idx + 1]
            result = row_resource.retrieve()
            self.assertIsInstance(result, Person)
            self.assertEqual(expected.id, row_resource.id)
            self.assertEqual(person.name, result.name)

    def test_retrieve_returns_none_for_negative_id(self):
        """PersonRowResource.retrieve() returns None for a negative ID
        """
        row_resource = self.table_resource[-1]
        result = row_resource.retrieve()
        self.assertIsNone(result)

    def test_retrieve_returns_none_for_missing_resource(self):
        """PersonRowResource.retrieve() returns None if no such person is found
        """
        row_resource = self.table_resource[999]
        result = row_resource.retrieve()
        self.assertIsNone(result)

    def test_update_returns_updated_person(self):
        """PersonRowResource.update() returns the correct Person object
        """
        target = self.people[1]
        changes = {'name': 'Our Lord and Savior, Nicolas Cage'}
        row_resource = self.table_resource[2]
        result = row_resource.update(changes)
        from ..models import Person
        self.assertIsInstance(result, Person)
        self.assertEqual(target.id, result.id)
        self.assertEqual(changes['name'], result.name)

    def test_update_updates_person(self):
        """PersonRowResource.update() successfully updates the correct person
        """
        changes = {'img_uri': 'https://upload.wikimedia.org/wikipedia/commons/3/33/Nicolas_Cage_2011_CC.jpg'}
        row_resource = self.table_resource[2]
        row_resource.update(changes)
        from ..models import Person
        result = DBSession.query(Person).filter_by(id=2).first()
        self.assertEqual(changes['img_uri'], result.img_uri)

    def test_update_only_changes_given_fields(self):
        """PersonRowResource.update() only updates the fields provided
        """
        target = self.people[1]
        changes = {'img_uri': 'https://upload.wikimedia.org/wikipedia/commons/3/33/Nicolas_Cage_2011_CC.jpg'}
        row_resource = self.table_resource[2]
        row_resource.update(changes)
        from ..models import Person
        result = DBSession.query(Person).filter_by(id=2).first()
        self.assertEqual(target.id, result.id)
        self.assertEqual(target.name, result.name)
        self.assertEqual(target.img_uri, changes['img_uri'])

    def test_update_does_nothing_with_unspecificed_fields(self):
        """PersonRowResource.update() completely ignores unspecified fields.
        """
        changes = {'is_bangin': True}
        row_resource = self.table_resource[2]
        result = row_resource.update(changes)
        self.assertIsNone(result)

    def test_update_update_returns_none_for_negative_id(self):
        """PersonRowResource.update() returns None if ID is negative
        """
        row_resource = self.table_resource[-1]
        changes = {'name': 'Our Lord and Savior, Nicolas Cage'}
        result = row_resource.update(changes)
        self.assertIsNone(result)

    def test_update_update_returns_none_for_missing_resource(self):
        """PersonRowResource.update() returns None if no such person is found
        """
        row_resource = self.table_resource[999]
        changes = {'name': 'Our Lord and Savior, Nicolas Cage'}
        result = row_resource.update(changes)
        self.assertIsNone(result)

    def test_update_does_nothing_for_negative_id(self):
        """PersonRowResource.update() makes no changes if ID is negative
        """
        row_resource = self.table_resource[-1]
        changes = {'name': 'Our Lord and Savior, Nicolas Cage'}
        row_resource.update(changes)
        from ..models import Person
        from . import PEOPLE
        for person in DBSession.query(Person):
            idx = person.id - 1
            self.assertEqual(PEOPLE[idx], person.name)

    def test_update_does_nothing_for_missing_resource(self):
        """PersonRowResource.update() makes no changes if no such person is found
        """
        row_resource = self.table_resource[999]
        changes = {'name': 'Our Lord and Savior, Nicolas Cage'}
        row_resource.update(changes)
        from ..models import Person
        from . import PEOPLE
        for person in DBSession.query(Person):
            idx = person.id - 1
            self.assertEqual(PEOPLE[idx], person.name)

    def test_update_does_not_raise_exception_with_none_uri(self):
        """PersonRowResource.update() does not throw an exception if 'None' is passed as a uri
        """
        row_resource = self.table_resource[1]
        changes = {
            'name': 'Our Lord and Savior, Nicolas Cage',
            'img_uri': None
        }
        try:
            row_resource.update(changes)
        except AttributeError as err:
            self.fail(err)

    def test_update_does_set_value_if_explicitly_none(self):
        """PersonRowResource.update() does not change a field with an updated value of 'None'
        """
        row_resource = self.table_resource[1]
        from ..models import Person
        expected_name = DBSession.query(Person).filter_by(id=1).first().name
        changes = {'name': None}
        row_resource.update(changes)
        person = DBSession.query(Person).filter_by(id=1).first()
        self.assertEqual(expected_name, person.name)

    def test_delete_works(self):
        """PersonRowResource.delete() successfully deletes the row
        """
        test_id = 2
        row_resource = self.table_resource[test_id]
        from ..models import Person
        row_resource.delete()
        db_ids = [x.id for x in DBSession.query(Person)]
        self.assertNotIn(test_id, db_ids)


class PersonTableResourceTests(PersonResourceTestCase):
    """
    Integration tests for :class:`resources.PersonTableResource` (effectively
    covers all test cases for :class:`resources.TableResource`).
    """

    def test_table_set(self):
        from ..models import Person
        self.assertEqual(self.table_resource.table, Person)

    def test_create_returns_person_object(self):
        """PersonTableResource.create() returns a new Person object based on input
        """
        person = {'name': 'Diane Lane'}
        result = self.table_resource.create(person)
        from ..models import Person
        self.assertIsInstance(result, Person)
        self.assertEqual('Diane Lane', result.name)

    def test_create_creates_person(self):
        """PersonTableResource.create() creates a person if everything checks out
        """
        person = {'name': 'Diane Lane'}
        self.table_resource.create(person)
        from ..models import Person
        result = DBSession.query(Person).filter_by(name='Diane Lane').first()
        self.assertEqual('Diane Lane', result.name)

    def test_create_ignores_explicit_id(self):
        """PersonTableResource.create() ignores an attempt to explicitly set an ID
        """
        person = {'name': 'Diane Lane', 'id': 999}
        result = self.table_resource.create(person)
        self.assertNotEqual(person['id'], result.id)

    def test_create_ignores_unauthorized_fields(self):
        """PersonTableResource.create() ignores unauthorized fields
        """
        person = {'name': 'Diane Lane', '_img_uri': 'http://www.images.com/something.jpg'}
        result = self.table_resource.create(person)
        self.assertNotEqual(person['_img_uri'], result.img_uri)

    def test_create_returns_none_for_unspecified_fields(self):
        """PersonTableResource.create() ignores unspecified fields
        """
        person = {'name': 'Diane Lane', 'status': 'Bangin\''}
        result = self.table_resource.create(person)
        with self.assertRaises(AttributeError):
            result.status

    def test_retrieve_returns_all(self):
        """PersonTableResource.retrieve() returns a full list of people without a filter
        """
        result = self.table_resource.retrieve()
        for person in self.people:
            self.assertTrue(person.name in [x.name for x in result])

    def test_retrieve_returns_filtered(self):
        """PersonTableResource.retrieve() returns a filtered list of people
        """
        query = {'name': 'Nicolas Cage'}
        result = self.table_resource.retrieve(query)
        self.assertEqual(1, len(result))
        from . import PEOPLE
        self.assertEqual(PEOPLE[0], result[0].name)

    def test_retrieve_returns_filtered_part(self):
        """PersonTableResource.retrieve() returns a filtered list of people who match a partial string
        """
        query = {'name': 'ch'}
        result = self.table_resource.retrieve(query)
        self.assertEqual(4, len(result))
        from . import PEOPLE
        self.assertEqual(PEOPLE[5], result[0].name)

    def test_retrieve_ignores_invalid_fields(self):
        """PersonTableResource.retrieve() ignores invalid fields in query
        """
        query = {'bad_field': 'Just plain bad.'}
        result = self.table_resource.retrieve(query)
        for person in self.people:
            self.assertTrue(person.name in [x.name for x in result])

    def test_getitem_returns_row_resource(self):
        """PersonTableResource.__getitem__() returns a PersonRowResource for all entities
        """
        from ..resources import PersonRowResource
        for idx, person in enumerate(self.people):
            row_resource = self.table_resource[idx]
            self.assertIsInstance(row_resource, PersonRowResource)

    def test_getitem_sets_row_resource_id(self):
        """PersonTableResource.__getitem__() correctly sets the PersonRowResource.id for all entities
        """
        for idx, person in enumerate(self.people):
            row_resource = self.table_resource[idx]
            self.assertEqual(row_resource.id, idx)

    def test_getitem_row_resource_table_set(self):
        """PersonTableResource.__getitem__() correctly sets the PersonRowResource.table for all entities
        """
        from ..models import Person
        for idx, person in enumerate(self.people):
            row_resource = self.table_resource[idx]
            self.assertEqual(row_resource.table, Person)


class FilmResourceTestCase(SQLiteTestCase):
    """
    A test case for FilmRowResource and FilmTableResource test suites.

    IMPORTANT NOTE: These tests are nowhere near as extensive as those for
    PersonRowResource and PersonTableResource because most of the tests for
    those two resources are, in fact, tests for the underlying RowResource and
    TableResources. Here we simply check to make sure FilmRowResource and
    FilmTableResource were defined correctly.
    """
    def setUp(self):
        super(FilmResourceTestCase, self).setUp()
        from ..resources import FilmTableResource
        self.table_resource = FilmTableResource(None, 'films', DBSession)
        self.films = []
        from . import FILMS
        from ..models import Film
        for title in FILMS:
            film = Film(title=title)
            self.films.append(film)
            DBSession.add(film)
        DBSession.commit()


class FilmRowResource(FilmResourceTestCase):
    """
    Integration tests for FilmRowResource.
    """

    def test_retrieve_works(self):
        """FilmRowResource.retrieve() returns the correct Person for all entities
        """
        from ..models import Film
        for idx, film in enumerate(self.films):
            expected = self.films[idx]
            row_resource = self.table_resource[idx + 1]
            result = row_resource.retrieve()
            self.assertIsInstance(result, Film)
            self.assertEqual(expected.id, row_resource.id)
            self.assertEqual(film.title, result.title)

    def test_update_updates_film(self):
        """FilmRowResource.update() successfully updates the correct film
        """
        changes = {'poster_uri': 'http://ia.media-imdb.com/images/M/MV5BNDg3MDM5NTI0MF5BMl5BanBnXkFtZTcwNDY0NDk0NA@@._V1_SX300.jpg'}
        row_resource = self.table_resource[2]
        row_resource.update(changes)
        from ..models import Film
        result = DBSession.query(Film).filter_by(id=2).first()
        self.assertEqual(changes['poster_uri'], result.poster_uri)


class FilmTableResourceTestCase(FilmResourceTestCase):
    """
    Integration tests for FilmTableResource.
    """

    def test_table_set(self):
        from ..models import Film
        self.assertEqual(self.table_resource.table, Film)

    def test_create_returns_film_object(self):
        """FilmTableResource.create() returns a new Film object based on input
        """
        film = {'title': 'Leaving Las Vegas'}
        result = self.table_resource.create(film)
        from ..models import Film
        self.assertIsInstance(result, Film)
        self.assertEqual('Leaving Las Vegas', result.title)

    def test_create_creates_person(self):
        """FilmTableResource.create() creates a film if everything checks out
        """
        film = {'title': 'Leaving Las Vegas'}
        self.table_resource.create(film)
        from ..models import Film
        result = DBSession.query(Film).filter_by(
            title='Leaving Las Vegas').first()
        self.assertEqual('Leaving Las Vegas', result.title)
