__author__ = 'kobnar'

from nose.plugins.attrib import attr
from . import DBSession, SQLiteTestCase


class PeopleAPIIndexViewsTests(SQLiteTestCase):
    def setUp(self):
        super(PeopleAPIIndexViewsTests, self).setUp()
        self.people = []
        from . import PEOPLE
        from ..models import Person
        for name in PEOPLE:
            person = Person(name=name)
            self.people.append(person)
            DBSession.add(person)
        DBSession.commit()
        self.view = self.compile_view()
        self.params = {'name': 'Nicolas Ford Coppola'}

    def compile_view(self):
        from ..views import PeopleAPIIndexViews
        from ..resources import PersonTableResource
        from pyramid.testing import DummyRequest
        request = DummyRequest()
        view_context = PersonTableResource(None, 'test_people', DBSession)
        return PeopleAPIIndexViews(view_context, request)

    def test_create_creates_person(self):
        """create() should successfully create a person
        """
        self.view.request.POST = self.params
        self.view.create()
        from ..models import Person
        output = DBSession.query(Person).filter_by(
            name=self.params['name']).first()
        self.assertIsNotNone(output.id)
        self.assertEqual(self.params['name'], output.name)

    def test_create_returns_201(self):
        """create() should return HTTP 201 if successful
        """
        self.view.request.POST = self.params
        self.view.create()
        from pyramid.httpexceptions import HTTPCreated
        response_code = self.view.request.response.status_int
        self.assertEqual(HTTPCreated.code, response_code)

    def test_create_includes_redirect_uri(self):
        """create() should return the new resource location
        """
        self.view.request.POST = self.params
        self.view.create()
        expected = '/api/v1/people/%s/' % str(len(self.people) + 1)
        location = self.view.request.response.location
        self.assertEqual(expected, location)

    def test_create_returns_new_resource_id(self):
        """create() should return the new resource id
        """
        self.view.request.POST = self.params
        output = self.view.create()
        try:
            new_id = output['id']
        except KeyError:
            self.fail('Resource ID not set')
        self.assertEqual(len(self.people) + 1, new_id)

    def test_create_without_fields_returns_400(self):
        """create() should return 400 if no fields are provided
        """
        self.view.create()
        from pyramid.httpexceptions import HTTPBadRequest
        response_code = self.view.request.response.status_int
        self.assertEqual(HTTPBadRequest.code, response_code)

    def test_create_without_fields_returns_no_location(self):
        """create() should not return a location if the name is empty, blank, etc.
        """
        self.view.create()
        location = self.view.request.response.location
        self.assertEqual(None, location)

    def test_create_without_name_returns_error(self):
        """create() should return a validation error if 'name' is not set
        """
        expected = {'name': 'Required'}
        output = self.view.create()
        self.assertEqual(expected, output)

    def test_create_without_name_returns_400(self):
        """create() should return 400 if the name is empty, blank, etc.
        """
        fields = {'name': None}
        self.view.request.POST = fields
        self.view.create()
        from pyramid.httpexceptions import HTTPBadRequest
        response_code = self.view.request.response.status_int
        self.assertEqual(HTTPBadRequest.code, response_code)

    def test_create_without_name_returns_no_location(self):
        """create() should not return a location if the name is empty, blank, etc.
        """
        fields = {'name': None}
        self.view.request.POST = fields
        self.view.create()
        location = self.view.request.response.location
        self.assertEqual(None, location)

    def test_create_duplicate_name_returns_400(self):
        """create() should return 400 if it was told to create a duplicate person
        """
        from . import PEOPLE
        for name in PEOPLE:
            fields = {'name': name}
            self.view.request.POST = fields
            self.view.create()
            from pyramid.httpexceptions import HTTPBadRequest
            response_code = self.view.request.response.status_int
            self.assertEqual(HTTPBadRequest.code, response_code)

    def test_create_duplicate_name_returns_empty(self):
        """create() should return an empty dict if it was told to create a duplicate person
        """
        from . import PEOPLE
        for name in PEOPLE:
            fields = {'name': name}
            self.view.request.POST = fields
            output = self.view.create()
            self.assertEqual({}, output)

    def test_retrieve_gets_everything(self):
        """retrieve() should return a list of everybody without an explicit query
        """
        output = self.view.retrieve()
        output_names = [x['name'] for x in output]
        people_names = [x.name for x in self.people]
        self.assertEqual(len(output_names), len(people_names))
        for name in people_names:
            self.assertTrue(name in output_names)
        for name in output_names:
            self.assertTrue(name in people_names)

    def test_retrieve_with_no_results_returns_404(self):
        """retrieve() should return 404 if no results matched the query
        """
        query = {'name': 'Nobody Atall'}
        self.view.request.GET = query
        self.view.retrieve()
        from pyramid.httpexceptions import HTTPNotFound
        response_code = self.view.request.response.status_int
        self.assertEqual(HTTPNotFound.code, response_code)

    def test_retrieve_with_invalid_query_returns_400(self):
        """retrieve() should return 400 if one of the query parameters was invalid
        """
        query = {'img_uri': 'not_a_uri'}
        self.view.request.GET = query
        self.view.retrieve()
        from pyramid.httpexceptions import HTTPBadRequest
        response_code = self.view.request.response.status_int
        self.assertEqual(HTTPBadRequest.code, response_code)

    def test_retrieve_returns_name_query(self):
        """retrieve() should return items related to a specific query
        """
        query = {'name': 'Nic'}
        self.view.request.GET = query
        output = self.view.retrieve()
        self.assertEqual(1, len(output))
        self.assertEqual(output[0]['name'], 'Nicolas Cage')


class PersonAPIViewsTests(SQLiteTestCase):
    def setUp(self):
        super(PersonAPIViewsTests, self).setUp()
        self.people = []
        from . import PEOPLE
        from ..models import Person
        for name in PEOPLE:
            person = Person(name=name)
            self.people.append(person)
            DBSession.add(person)
        DBSession.commit()
        self.params = {'name': 'Nicolas Ford Coppola'}

    def compile_view(self, row_id):
        from ..views import PersonAPIViews
        from ..resources import PersonTableResource
        table_resource = PersonTableResource(None, 'people')
        from ..resources import PersonRowResource
        from pyramid.testing import DummyRequest
        request = DummyRequest()
        view_context = PersonRowResource(table_resource, row_id, DBSession)
        return PersonAPIViews(view_context, request)

    def test_retrieve_works(self):
        """retrieve() should return the appropriate person instance
        """
        for person in self.people:
            view = self.compile_view(person.id)
            result = view.retrieve()
            self.assertEqual(person.id, result['id'])
            self.assertEqual(person.name, result['name'])

    def test_retrieve_returns_404_with_unregistered_id(self):
        """retrieve() should return status code 400 with an unregistered ID
        """
        view = self.compile_view(999)
        view.retrieve()
        from pyramid.httpexceptions import HTTPNotFound
        response_code = view.request.response.status_int
        self.assertEqual(HTTPNotFound.code, response_code)

    def test_retrieve_returns_400_with_invalid_id(self):
        """retrieve() should return status code 400 with an invalid ID
        """
        view = self.compile_view(-1)
        view.retrieve()
        from pyramid.httpexceptions import HTTPBadRequest
        response_code = view.request.response.status_int
        self.assertEqual(HTTPBadRequest.code, response_code)

    def test_retrieve_returns_errors_with_zero_id(self):
        """retrieve() should return a dictionary of errors with a zero ID
        """
        view = self.compile_view(0)
        result = view.retrieve()
        self.assertEqual({'id': '0 is less than minimum value 1'}, result)

    def test_retrieve_returns_errors_with_negative_id(self):
        """retrieve() should return a dictionary of errors with a negative ID
        """
        view = self.compile_view(-1)
        result = view.retrieve()
        self.assertEqual({'id': '-1 is less than minimum value 1'}, result)

    def test_retrieve_returns_only_specified_fields(self):
        """retrieve() should return a dictionary of errors with a negative ID
        """
        view = self.compile_view(1)
        view.request.GET = {'fields': ['name']}
        result = view.retrieve()
        self.assertTrue('name' in result.keys())
        self.assertFalse('id' in result.keys())
        self.assertFalse('img_uri' in result.keys())
        self.assertFalse('producer_credits' in result.keys())
