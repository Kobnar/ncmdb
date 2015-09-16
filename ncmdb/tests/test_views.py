__author__ = 'kobnar'
from nose.plugins.attrib import attr
from . import DBSession, SQLiteTestCase


class ViewsTestCase(SQLiteTestCase):
    def setUp(self):
        super(ViewsTestCase, self).setUp()
        self.people = []
        from . import NAMES
        from ..models import Person
        for name in NAMES:
            person = Person(name=name)
            self.people.append(person)
            DBSession.add(person)
        DBSession.commit()

    def compile_view(self, view, context):
        from pyramid.testing import DummyRequest
        request = DummyRequest()
        view_context = context(None, 'test_people', DBSession)
        return view(view_context, request)


class PersonAPIViewsTests(ViewsTestCase):
    def test_retrieve_gets_everything(self):
        """people/ GET should return a list of everybody if it doesn't have any qualifiers
        """
        from ..views import PersonIndexAPIViews
        from ..resources import PersonTableResource
        view = self.compile_view(PersonIndexAPIViews, PersonTableResource)
        output = view.retrieve()
        output_names = [x['name'] for x in output]
        people_names = [x.name for x in self.people]
        self.assertEqual(len(output_names), len(people_names))
        for name in people_names:
            self.assertTrue(name in output_names)
        for name in output_names:
            self.assertTrue(name in people_names)

    def test_retrieve_with_name_query_gets_matching_queries(self):
        """people/ GET should return a smaller list
        """
        from ..views import PersonIndexAPIViews
        from ..resources import PersonTableResource
        query = {'name': 'Nick'}
        view = self.compile_view(
            PersonIndexAPIViews, PersonTableResource)
        view.request.params = query
        output = view.retrieve()
        self.assertEqual(1, len(output))
        self.assertEqual('Nick Cage', output[0]['name'])

    @attr('todo')
    def test_retrieve_with_id_img_uri_gets_matching_queries(self):
        self.fail()

    @attr('todo')
    def test_retrieve_with_id_query_gets_only_one_reply(self):
        self.fail()

    def test_retireve_returns_404_with_bad_query(self):
        query = {'bad_field': 'Just plain bad.'}
        from ..views import PersonIndexAPIViews
        from ..resources import PersonTableResource
        view = self.compile_view(
            PersonIndexAPIViews, PersonTableResource)
        view.request.params = query
        view.retrieve()
        from pyramid.exceptions import HTTPNotFound
        self.assertEqual(HTTPNotFound.code, view.request.response.status_int)

    def test_retireve_returns_nothing_with_bad_query(self):
        query = {'bad_field': 'Just plain bad.'}
        from ..views import PersonIndexAPIViews
        from ..resources import PersonTableResource
        view = self.compile_view(
            PersonIndexAPIViews, PersonTableResource)
        view.request.params = query
        output = view.retrieve()
        self.assertEqual(0, len(output))
