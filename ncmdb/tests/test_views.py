__author__ = 'kobnar'
from nose.plugins.attrib import attr
from . import DBSession, SQLiteTestCase


class ViewsTestCase(SQLiteTestCase):
    def setUp(self):
        super(ViewsTestCase, self).setUp()
        self.people = []
        from . import PEOPLE
        from ..models import Person
        for name in PEOPLE:
            person = Person(name=name)
            self.people.append(person)
            DBSession.add(person)
        DBSession.commit()

    def compile_view(self, view, context):
        from pyramid.testing import DummyRequest
        request = DummyRequest()
        view_context = context(None, 'test_people', DBSession)
        return view(view_context, request)


class PeopleAPIIndexViewsTests(ViewsTestCase):
    def setUp(self):
        super(PeopleAPIIndexViewsTests, self).setUp()
        from ..views import PeopleAPIIndexViews
        from ..resources import PersonTableResource
        self.view = self.compile_view(PeopleAPIIndexViews, PersonTableResource)
        self.params = {'name': 'Nicolas Ford Coppola'}

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
