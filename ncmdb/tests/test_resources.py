from unittest import TestCase
from nose.plugins.attrib import attr
from ..resources import IndexResource, RowResource, TableResource
from . import DBSession, SQLiteTestCase, MockTable

__author__ = 'kobnar'


class _MockResourceTable(MockTable):
    """
    A mock resource table used for integration testing Pyramid's traversal
    resources.
    """
    FIELD_CHOICES = ['name']
    from sqlalchemy import Column, String
    name = Column(String)
    __mapper_args__ = {
        'polymorphic_identity': 'mock_res_table'
    }


class _MockRowResource(RowResource):
    """
    A mock row resource for testing traversal resources.
    """


class _MockTableResource(TableResource):
    """
    A mock table resource for testing traversal resources.
    """
    _table = _MockResourceTable
    _row_resource = _MockRowResource


class IndexResourceTestCase(TestCase):
    """
    Unit tests for :class:`resources.IndexResource`.
    """

    def make_root(self):
        self.root = IndexResource(None, 'root')

    def test_init_sets_parent(self):
        """IndexResource.__init__() sets the correct parent
        """
        self.make_root()
        child = IndexResource(self.root, 'child')
        self.assertEqual(child.__parent__, self.root)

    def test_init_parent_accepts_none(self):
        """IndexResource.__init__() accepts 'None' as 'parent'
        """
        try:
            IndexResource(None, 'root')
        except TypeError as err:
            self.fail(err)

    def test_init_parent_accepts_index_resource(self):
        """IndexResource.__init__() accepts an IndexResource as 'parent'
        """
        self.make_root()
        try:
            IndexResource(self.root, 'index')
        except TypeError as err:
            self.fail(err)

    def test_init_parent_raises_exception_if_parent_is_bad_type(self):
        """IndexResource.__init__() raises an exception if 'parent' is not an IndexResource or 'None'
        """
        non_strings = [
            False,
            True,
            1,
            1.1,
            'string']
        for x in non_strings:
            with self.assertRaises(TypeError):
                IndexResource(x, 'index')

    def test_init_name_accepts_string(self):
        """IndexResource.__init__() accepts a string as 'name'
        """
        try:
            IndexResource(None, 'index')
        except TypeError as err:
            self.fail(err)

    def test_init_sets_name(self):
        """IndexResource.__init__() sets the correct name
        """
        self.make_root()
        child = IndexResource(self.root, 'child')
        self.assertEqual(child.__name__, 'child')

    def test_init_name_raises_exception_for_non_strings(self):
        """IndexResource.__init__() raises  an exception if 'name' is not a string
        """
        non_strings = [
            None,
            False,
            True,
            1, 1.1,
            IndexResource(None, 'index')]
        for x in non_strings:
            with self.assertRaises(TypeError):
                IndexResource(None, x)

    def test_setitem_sets_names(self):
        """IndexResource.__setitem__() sets the correct name
        """
        self.make_root()
        self.root['1'] = IndexResource
        self.root['1']['1.1'] = IndexResource
        self.root['2'] = IndexResource
        self.root['2']['2.1'] = IndexResource
        self.root['2']['2.1']['2.1.1'] = IndexResource
        self.root['2']['2.2'] = IndexResource
        self.assertEqual(
            self.root['1'].__name__,
            '1')
        self.assertEqual(
            self.root['1']['1.1'].__name__,
            '1.1')
        self.assertEqual(
            self.root['2'].__name__,
            '2')
        self.assertEqual(
            self.root['2']['2.1'].__name__,
            '2.1')
        self.assertEqual(
            self.root['2']['2.1']['2.1.1'].__name__,
            '2.1.1')
        self.assertEqual(
            self.root['2']['2.2'].__name__,
            '2.2')

    def test_setitem_sets_parents(self):
        """IndexResource.__setitem__() sets the correct parent
        """
        self.make_root()
        self.root['1'] = IndexResource
        self.root['1']['1.1'] = IndexResource
        self.root['2'] = IndexResource
        self.root['2']['2.1'] = IndexResource
        self.root['2']['2.1']['2.1.1'] = IndexResource
        self.root['2']['2.2'] = IndexResource
        self.assertEqual(
            self.root['1'].__parent__,
            self.root)
        self.assertEqual(
            self.root['1']['1.1'].__parent__,
            self.root['1'])
        self.assertEqual(
            self.root['2'].__parent__,
            self.root)
        self.assertEqual(
            self.root['2']['2.1'].__parent__,
            self.root['2'])
        self.assertEqual(
            self.root['2']['2.1']['2.1.1'].__parent__,
            self.root['2']['2.1'])
        self.assertEqual(
            self.root['2']['2.2'].__parent__,
            self.root['2'])

    def test_setitem_raises_exception_if_item_is_not_an_indexresource(self):
        """IndexResource.__setitem__() raises an exception if the item is not a type of IndexResource
        """
        self.make_root()
        from ..models import Person
        with self.assertRaises(TypeError):
            self.root['index'] = Person


class _MockResourceTestCase(SQLiteTestCase):
    """
    A wrapper to setup test data for resource tests.
    """
    def setUp(self):
        super(_MockResourceTestCase, self).setUp()
        self.tbl_rec = _MockTableResource(None, 'mock_table', DBSession)

    def make_data(self):
        self.row_names = ['doc 1', 'document 2', 'dox 3']
        for name in self.row_names:
            doc = _MockResourceTable(name=name)
            DBSession.add(doc)
        DBSession.flush()
        query = DBSession.query(_MockResourceTable).all()
        self.row_ids = [x.id for x in query]


@attr('sqlalchemy')
class TableResourceTests(_MockResourceTestCase):
    """
    Integration tests for :class:`resources.TableResource`.
    """

    def test_getitem_accepts_int(self):
        """TableResource.__getitem__() accepts an integer
        """
        id = 123
        try:
            self.tbl_rec[id]
        except KeyError as err:
            self.fail(err)

    def test_getitem_accepts_int_string(self):
        """TableResource.__getitem__() accepts a string-formatted integer
        """
        id = '123'
        try:
            self.tbl_rec[id]
        except KeyError as err:
            self.fail(err)

    def test_getitem_returns_child_index(self):
        """TableResource.__getitem__() returns a child IndexResource if it is not an integer
        """
        self.tbl_rec['index'] = IndexResource
        result = self.tbl_rec['index']
        self.assertIsInstance(result, IndexResource)
        self.assertEqual(result.__name__, 'index')

    def test_getitem_raises_key_error_for_invalid_int_string_if_not_child(self):
        """TableResource.__getitem__() raises `KeyError` if `name' is not an ObjectId or child name
        """
        with self.assertRaises(KeyError):
            self.tbl_rec['nonsense']

    def test_table_is_read_only(self):
        """TableResource.table is read-only
        """
        with self.assertRaises(AttributeError):
            self.tbl_rec.table = _MockResourceTable

    def test_table_is_set(self):
        """TableResource.table is set correctly
        """
        self.assertEqual(self.tbl_rec.table, _MockResourceTable)

    def test_create_requires_data(self):
        """TableResource.create() raises exception if no data is provided
        """
        with self.assertRaises(AssertionError):
            self.tbl_rec.create(None)

    def test_create_returns_mock_row(self):
        """TableResource.create() returns a new row object
        """
        data = {'name': 'doc 4'}
        row = self.tbl_rec.create(data)
        self.assertIsInstance(row, _MockResourceTable)

    def test_create_sets_value(self):
        """TableResource.create() sets correct values
        """
        data = {'name': 'doc 4'}
        row = self.tbl_rec.create(data)
        self.assertEqual(row.name, data['name'])

    def test_create_saves_to_sqlalchemy(self):
        """TableResource.create() saves a new row in SQLAlchemy
        """
        data = {'name': 'doc 4'}
        row = self.tbl_rec.create(data)
        result = DBSession.query(_MockResourceTable).filter_by(id=row.id).first()
        self.assertIsInstance(result, _MockResourceTable)

    def test_create_sets_values_in_sqlalchemy(self):
        """TableResource.create() sets correct values to new row in SQLAlchemy
        """
        data = {'name': 'doc 4'}
        row = self.tbl_rec.create(data)
        result = DBSession.query(_MockResourceTable).filter_by(id=row.id).first()
        self.assertEqual(result.name, row.name)

    def test_retrieve_returns_all_rows_without_query(self):
        """TableResource.retrieve() returns all rows if no query is provided
        """
        self.make_data()
        results = self.tbl_rec.retrieve()
        names = [x.name for x in results]
        self.assertEqual(len(results), 3)
        for x in results:
            self.assertIn(x.name, names)

    def test_retrieve_returns_matching_rows(self):
        """TableResource.retrieve() returns all rows matching query
        """
        self.make_data()
        query = {'name': 'doc'}
        results = self.tbl_rec.retrieve(query)
        names = [x.name for x in results]
        self.assertEqual(len(results), 2)
        for x in results:
            self.assertIn(x.name, names)


@attr('sqlalchemy')
class RowResourceTests(_MockResourceTestCase):
    """
    Integration tests for :class:`resources.RowResource`.
    """
    def setUp(self):
        super(RowResourceTests, self).setUp()
        self.make_data()
        self.row_rec = self.tbl_rec[self.row_ids[0]]

    def test_id_is_read_only(self):
        """RowResource.id is read-only
        """
        with self.assertRaises(AttributeError):
            self.row_rec.id = 123

    def test_id_is_int(self):
        """RowResource.id returns an integer
        """
        self.assertIsInstance(self.row_rec.id, int)

    def test_id_is_correct_int(self):
        """RowResource.id is properly set as target ID
        """
        self.assertEqual(self.row_rec.id, self.row_ids[0])

    def test_table_is_read_only(self):
        """RowResource.table is read-only
        """
        with self.assertRaises(AttributeError):
            self.row_rec.table = 'string'

    def test_table_is_parent_table(self):
        """RowResource.table is the same as it's parent's
        """
        self.assertEqual(
            self.row_rec.table,
            self.tbl_rec.table)

    def test_retrieve_returns_row(self):
        """RowResource.retrieve() returns a row if it exists
        """
        result = self.row_rec.retrieve()
        result_id = result.id
        self.assertIsInstance(result, _MockResourceTable)
        self.assertEqual(result_id, self.row_ids[0])

    def test_retrieve_returns_none_if_does_not_exist(self):
        """RowResource.retrieve() returns `None` if row does not exist
        """
        obj_id = 999
        bad_row_rec = self.tbl_rec[obj_id]
        result = bad_row_rec.retrieve()
        self.assertIsNone(result)

    def test_update_returns_true(self):
        """RowResource.update() returns `True` if update was successful
        """
        update = {'name': 'new name'}
        result = self.row_rec.update(update)
        self.assertTrue(result)

    def test_update_saves_to_sqlite(self):
        """RowResource.update() saves changes to SQLite
        """
        update = {'name': 'new name'}
        self.row_rec.update(update)
        result = DBSession.query(_MockResourceTable).filter_by(
            id=self.row_ids[0]).first()
        self.assertEqual(result.name, update['name'])

    def test_update_returns_false_if_does_not_exist(self):
        """RowResource.update() returns `False` if row does not exist
        """
        obj_id = 999
        bad_row_rec = self.tbl_rec[obj_id]
        update = {'name': 'new name'}
        result = bad_row_rec.update(update)
        self.assertFalse(result)

    def test_delete_removes_from_sqlite(self):
        """RowResource.delete() removes the row from SQLite
        """
        self.row_rec.delete()
        result = DBSession.query(_MockResourceTable).filter_by(
            id=self.row_ids[0]).first()
        self.assertFalse(result)


class _PersonResourceTestCase(SQLiteTestCase):
    """
    A test case for PersonTableResource and PersonRowResource test suites.
    """
    def setUp(self):
        super(_PersonResourceTestCase, self).setUp()
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


class PersonRowResourceTests(_PersonResourceTestCase):
    """
    Integration tests for :class:`resources.PersonRowResource` (effectively
    duplicates all test cases for :class:`resources.RowResource`).
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
        changes = {'image_uri': 'https://upload.wikimedia.org/wikipedia/commons/3/33/Nicolas_Cage_2011_CC.jpg'}
        row_resource = self.table_resource[2]
        row_resource.update(changes)
        from ..models import Person
        result = DBSession.query(Person).filter_by(id=2).first()
        self.assertEqual(changes['image_uri'], result.image_uri)

    def test_update_only_changes_given_fields(self):
        """PersonRowResource.update() only updates the fields provided
        """
        target = self.people[1]
        changes = {'image_uri': 'https://upload.wikimedia.org/wikipedia/commons/3/33/Nicolas_Cage_2011_CC.jpg'}
        row_resource = self.table_resource[2]
        row_resource.update(changes)
        from ..models import Person
        result = DBSession.query(Person).filter_by(id=2).first()
        self.assertEqual(target.id, result.id)
        self.assertEqual(target.name, result.name)
        self.assertEqual(target.image_uri, changes['image_uri'])

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
            'image_uri': None
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


class PersonTableResourceTests(_PersonResourceTestCase):
    """
    Integration tests for :class:`resources.PersonTableResource` (effectively
    duplicates all test cases for :class:`resources.TableResource`).
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
        person = {'name': 'Diane Lane', '_image_uri': 'http://www.images.com/something.jpg'}
        result = self.table_resource.create(person)
        self.assertNotEqual(person['_image_uri'], result.image_uri)

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

    def test_retrieve_returns_filtered_partial_string(self):
        """PersonTableResource.retrieve() returns a filtered list of people who match a partial string
        """
        query = {'name': 'ch'}
        result = self.table_resource.retrieve(query)
        self.assertEqual(4, len(result))
        from . import PEOPLE
        self.assertEqual(PEOPLE[5], result[0].name)

    def test_retrieve_ignores_explicit_id(self):
        """PersonTableResource.retrieve() ignores an explicit ID
        """
        query = {'id': 5}
        result = self.table_resource.retrieve(query)
        for person in self.people:
            self.assertTrue(person.name in [x.name for x in result])

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

    def test_non_int_does_not_fetch_row_resource(self):
        """PersonTableresource.__getitem__() does not set a PersonRowResource if child context is not an integer
        """
        with self.assertRaises(KeyError):
            self.table_resource['string']


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
