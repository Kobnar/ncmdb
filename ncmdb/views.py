__author__ = 'kobnar'

from pyramid.view import view_defaults, view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPCreated, HTTPBadRequest
from colander import Invalid

from .resources import IndexResource, PersonTableResource, PersonRowResource,\
    FilmTableResource, FilmRowResource
from .schema import IdSchema, CreatePersonSchema, RetrievePeopleSchema, \
    RetrievePersonSchema, UpdatePersonSchema, \
    CreateFilmSchema, UpdateFilmSchema, RetrieveFilmsSchema, \
    RetrieveFilmSchema


class BaseView(object):
    """
    Provides a default view configuration for common view elements and output.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request


@view_defaults(context=IndexResource)
class IndexViews(BaseView):
    """/
    """

    @view_config(renderer='index/home.jinja2')
    def home(self):
        schema = RetrieveFilmsSchema()
        try:
            data = schema.deserialize(self.request.GET)
            print(data)
        except Invalid:
            self.request.response.status_int = HTTPNotFound.code
            return {'films': []}
        film_resource = FilmTableResource(self.context, 'films')
        films = [x.serialize() for x in film_resource.retrieve(data)]
        return {'films': films}


@view_defaults(context=PersonTableResource, renderer='json')
class PeopleAPIIndexViews(BaseView):
    """/api/v1/people/
    """

    @view_config(request_method='POST')
    def create(self):

        # Instantiate the CREATE Colander schema:
        schema = CreatePersonSchema()

        # Validate POST data, return '400 Bad Request' if it fails:
        try:
            data = schema.deserialize(self.request.POST)
        except Invalid as err:
            self.request.response.status_int = HTTPBadRequest.code
            return err.asdict()

        # Create a new Person:
        result = self.context.create(data)

        if result:
            # If created, return ID, location, etc.:
            self.request.response.status_int = HTTPCreated.code
            self.request.response.location = '/api/v1/people/%s/' \
                                             % str(result.id)
            return {'id': result.id}

        # If it fails, assume it is a duplicate:
        self.request.response.status_int = HTTPBadRequest.code
        return {'name': 'Person exists'}

    @view_config(request_method='GET')
    def retrieve(self):
        # Instantiate the RETRIEVE Colander schema:
        schema = RetrievePeopleSchema()
        try:
            data = schema.deserialize(self.request.GET)
        except Invalid as err:
            self.request.response.status_int = HTTPBadRequest.code
            return err.asdict()
        result = self.context.retrieve(data)
        if not result:
            self.request.response.status_int = HTTPNotFound.code
        return result


@view_defaults(context=PersonRowResource, renderer='json')
class PersonAPIViews(BaseView):
    """/api/v1/people/{#}/
    """

    @view_config(request_method='GET')
    def retrieve(self):
        id_schema = IdSchema()
        fields_schema = RetrievePersonSchema()
        try:
            id_schema.deserialize({'id': self.context.id})
            data = fields_schema.deserialize(self.request.GET)
        except Invalid as err:
            self.request.response.status_int = HTTPBadRequest.code
            return err.asdict()
        result = self.context.retrieve()
        if result:
            if data['fields']:
                result = {k: v for k, v in result.items()
                          if k in data['fields']}
            return result
        self.request.response.status_int = HTTPNotFound.code
        return {}

    @view_config(request_method='PUT')
    def update(self):
        id_schema = IdSchema()
        row_schema = UpdatePersonSchema()
        try:
            id_schema.deserialize({'id': self.context.id})
            data = row_schema.deserialize(self.request.POST)
        except Invalid as err:
            self.request.response.status_int = HTTPBadRequest.code
            return err.asdict()
        result = self.context.update(data)
        if result:
            return result
        self.request.response.status_int = HTTPBadRequest.code
        return {}

    @view_config(request_method='DELETE')
    def delete(self):
        id_schema = IdSchema()
        try:
            id_schema.deserialize({'id': self.context.id})
        except Invalid as err:
            self.request.response.status_int = HTTPBadRequest.code
            return err.asdict()
        self.context.delete()
        return {}


@view_defaults(context=FilmTableResource, renderer='json')
class FilmsAPIIndexViews(BaseView):
    """/api/v1/films/
    """

    @view_config(request_method='POST')
    def create(self):
        schema = CreateFilmSchema()
        try:
            data = schema.deserialize(self.request.POST)
        except Invalid as err:
            self.request.response.status_int = HTTPBadRequest.code
            return err.asdict()
        result = self.context.create(data)
        if result:
            self.request.response.status_int = HTTPCreated.code
            self.request.response.location = '/api/v1/people/%s/' \
                                             % str(result.id)
            return {'id': result.id}
        self.request.response.status_int = HTTPBadRequest.code
        return {}

    @view_config(request_method='GET')
    def retrieve(self):
        schema = RetrieveFilmsSchema()
        try:
            data = schema.deserialize(self.request.GET)
        except Invalid as err:
            self.request.response.status_int = HTTPBadRequest.code
            return err.asdict()
        result = self.context.retrieve(data)
        if not result:
            self.request.response.status_int = HTTPNotFound.code
        return result


@view_defaults(context=FilmRowResource, renderer='json')
class FilmAPIViews(BaseView):
    """/api/v1/films/{#}/
    """

    @view_config(request_method='GET')
    def retrieve(self):
        id_schema = IdSchema()
        fields_schema = RetrieveFilmSchema()
        try:
            id_schema.deserialize({'id': self.context.id})
            data = fields_schema.deserialize(self.request.GET)
        except Invalid as err:
            self.request.response.status_int = HTTPBadRequest.code
            return err.asdict()
        result = self.context.retrieve()
        if result:
            if data['fields']:
                result = {k: v for k, v in result.items()
                          if k in data['fields']}
            return result
        self.request.response.status_int = HTTPNotFound.code
        return {}

    @view_config(request_method='PUT')
    def update(self):
        id_schema = IdSchema()
        row_schema = UpdateFilmSchema()
        try:
            id_schema.deserialize({'id': self.context.id})
            data = row_schema.deserialize(self.request.POST)
        except Invalid as err:
            self.request.response.status_int = HTTPBadRequest.code
            return err.asdict()
        result = self.context.update(data)
        if result:
            return result
        self.request.response.status_int = HTTPBadRequest.code
        return {}

    @view_config(request_method='DELETE')
    def delete(self):
        id_schema = IdSchema()
        try:
            id_schema.deserialize({'id': self.context.id})
        except Invalid as err:
            self.request.response.status_int = HTTPBadRequest.code
            return err.asdict()
        self.context.delete()
        return {}
