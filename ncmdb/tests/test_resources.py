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
        from . import NAMES
        from ..models import Person
        for name in NAMES:
            person = Person(name=name)
            self.people.append(person)
            DBSession.add(person)
        DBSession.commit()


class PersonTableResourceTests(PersonResourceTestCase):

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
        self.assertEqual('Nicolas Cage', result[0].name)

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


class PersonRowResourceTests(PersonResourceTestCase):

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
        """PersonRowResource.update() updates the correct Person
        """
        target = self.people[1]
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

    def test_delete_works(self):
        """PersonRowResource.delete() successfully deletes the row
        """
        row_resource = self.table_resource[2]
        from ..models import Person
        pre_check = DBSession.query(Person).filter_by(id=2).first()
        self.assertIsNotNone(pre_check)
        row_resource.delete()
        result = DBSession.query(Person).filter_by(id=2).first()
        self.assertIsNone(result)


class FilmResourceTestCase(SQLiteTestCase):
    """
    A test case for PersonTableResource and PersonRowResource test suites.
    """
    def setUp(self):
        super(FilmResourceTestCase, self).setUp()
        from ..resources import FilmTableResource
        self.table_resource = FilmTableResource(None, 'films', DBSession)
        self.films = []
        from . import FILMS
        from ..models import Film
        for film in FILMS:
            film = Film(**film)
            self.films.append(film)
            DBSession.add(film)
        DBSession.commit()

    def test_film_resources(self):
        self.fail('Film resources need tests too, buddy.')
