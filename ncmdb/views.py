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

        # Instantiate main search schema:
        schema = RetrieveFilmsSchema()

        # Validate schema:
        try:
            data = schema.deserialize(self.request.GET)
            print(data)
        except Invalid:
            self.request.response.status_int = HTTPNotFound.code
            return {'films': []}

        # Fetch and return a list of films matching query:
        film_resource = FilmTableResource(self.context, 'films')
        films = [x.serialize() for x in film_resource.retrieve(data)]
        return {'films': films}


@view_defaults(context=PersonTableResource, renderer='json')
class PeopleAPIIndexViews(BaseView):
    """/api/v1/people/
    """

    @view_config(request_method='POST')
    def create(self):

        # Instantiate schema to CREATE a person:
        schema = CreatePersonSchema()

        # Validate POST data (return '400 Bad Request' if it fails):
        try:
            data = schema.deserialize(self.request.POST)
        except Invalid as err:
            self.request.response.status_int = HTTPBadRequest.code
            return err.asdict()

        # Create a new Person with validated data:
        result = self.context.create(data)

        # If successful, return '201 Created', the location of the object, and
        # the new person's ID.
        if result:
            self.request.response.status_int = HTTPCreated.code
            self.request.response.location = '/api/v1/people/{}/'.\
                format(str(result.id))
            return {'id': result.id}

        # If failed, assume it was a duplicate:
        self.request.response.status_int = HTTPBadRequest.code
        return {'name': 'Person exists'}

    @view_config(request_method='GET')
    def retrieve(self):

        # Instantiate schema to RETRIEVE a list of people:
        schema = RetrievePeopleSchema()

        # Validate form data:
        try:
            data = schema.deserialize(self.request.GET)
        except Invalid as err:
            self.request.response.status_int = HTTPBadRequest.code
            return err.asdict()

        # RETRIEVE the P:
        result = self.context.retrieve(data)

        # If found, serialize and return a list of people:
        if result:
            return [x.serialize() for x in result]

        # If list is empty, return '404 Not Found':
        self.request.response.status_int = HTTPNotFound.code
        return []


@view_defaults(context=PersonRowResource, renderer='json')
class PersonAPIViews(BaseView):
    """/api/v1/people/{#}/
    """

    @view_config(request_method='GET')
    def retrieve(self):

        # Instantiate schemas to validate ID and RETRIEVE a person:
        id_schema = IdSchema()
        fields_schema = RetrievePersonSchema()

        # Validate form data:
        try:
            id_schema.deserialize({'id': self.context.id})
            data = fields_schema.deserialize(self.request.GET)
        except Invalid as err:
            self.request.response.status_int = HTTPBadRequest.code
            return err.asdict()

        # RETRIEVE Person:
        result = self.context.retrieve()

        # If found, serialize Person:
        if result:
            result = result.serialize()
            if data['fields']:
                result = {k: v for k, v in result.items()
                          if k in data['fields']}
            return result

        # Return '404 Not Found' if Person does not exist:
        self.request.response.status_int = HTTPNotFound.code
        return {}

    @view_config(request_method='PUT')
    def update(self):

        # Instantiate schemas to validate ID and UPDATE a person:
        id_schema = IdSchema()
        row_schema = UpdatePersonSchema()

        # Validate form data:
        try:
            id_schema.deserialize({'id': self.context.id})
            data = row_schema.deserialize(self.request.POST)
        except Invalid as err:
            self.request.response.status_int = HTTPBadRequest.code
            return err.asdict()

        # Update the Person:
        result = self.context.update(data)

        # If update successful, serialize output:
        if result:
            return result.serialize()

        # Return '400 Bad Request' if update failed:
        self.request.response.status_int = HTTPBadRequest.code
        # TODO: distinguish between 400 and 404 errors!
        return {}

    @view_config(request_method='DELETE')
    def delete(self):

        # Instantiate schema to validate ID:
        id_schema = IdSchema()

        # Validate ID:
        try:
            id_schema.deserialize({'id': self.context.id})
        except Invalid as err:
            self.request.response.status_int = HTTPBadRequest.code
            return err.asdict()

        # Delete Person and return 'None':
        self.context.delete()
        return None


@view_defaults(context=FilmTableResource, renderer='json')
class FilmsAPIIndexViews(BaseView):
    """/api/v1/films/
    """

    @view_config(request_method='POST')
    def create(self):

        # Instantiate schema to CREATE a Film:
        schema = CreateFilmSchema()

        # Validate POST data:
        try:
            data = schema.deserialize(self.request.POST)
        except Invalid as err:
            self.request.response.status_int = HTTPBadRequest.code
            return err.asdict()

        # Create new film:
        result = self.context.create(data)

        # If successful, return '201 Created', new location and the film's ID:
        if result:
            self.request.response.status_int = HTTPCreated.code
            self.request.response.location = '/api/v1/people/%s/'.\
                format(str(result.id))
            return {'id': result.id}

        # If failed, return '400 Bad Request':
        self.request.response.status_int = HTTPBadRequest.code
        return {}

    @view_config(request_method='GET')
    def retrieve(self):

        # Instantiate schema to RETRIEVE a list of films:
        schema = RetrieveFilmsSchema()

        # Validate query data:
        try:
            data = schema.deserialize(self.request.GET)
        except Invalid as err:
            self.request.response.status_int = HTTPBadRequest.code
            return err.asdict()

        # Retrieve a list of films:
        result = self.context.retrieve(data)

        # Return a list of films matching query:
        if result:
            return [x.serialize() for x in result]

        # If nothing was found, return a '404 Not Found' code and an empty list:
        self.request.response.status_int = HTTPNotFound.code
        return []


@view_defaults(context=FilmRowResource, renderer='json')
class FilmAPIViews(BaseView):
    """/api/v1/films/{#}/
    """

    @view_config(request_method='GET')
    def retrieve(self):

        # Instantiate schemas to validate ID and RETRIEVE a film:
        id_schema = IdSchema()
        fields_schema = RetrieveFilmSchema()

        # Validate query data:
        try:
            id_schema.deserialize({'id': self.context.id})
            data = fields_schema.deserialize(self.request.GET)
        except Invalid as err:
            self.request.response.status_int = HTTPBadRequest.code
            return err.asdict()

        # Retrieve person:
        result = self.context.retrieve()

        # If found, serialize output:
        if result:
            if data['fields']:
                result = {k: v for k, v in result.items()
                          if k in data['fields']}
            return result

        # Return '404 Not Found' if Film does not exist:
        self.request.response.status_int = HTTPNotFound.code
        return {}

    @view_config(request_method='PUT')
    def update(self):

        # Instantiate schemas to validate ID and UPDATE a film:
        id_schema = IdSchema()
        row_schema = UpdateFilmSchema()

        # Validate form data:
        try:
            id_schema.deserialize({'id': self.context.id})
            data = row_schema.deserialize(self.request.POST)
        except Invalid as err:
            self.request.response.status_int = HTTPBadRequest.code
            return err.asdict()

        # Update film:
        result = self.context.update(data)

        # If successful, return film:
        if result:
            return result.serialize()

        # Return '400 Bad Request' if update failed:
        self.request.response.status_int = HTTPBadRequest.code
        # TODO: distinguish between 400 and 404 errors!
        return {}

    @view_config(request_method='DELETE')
    def delete(self):
        # Instantiate schema to validate an ID:
        id_schema = IdSchema()

        # Validate the ID:
        try:
            id_schema.deserialize({'id': self.context.id})
        except Invalid as err:
            self.request.response.status_int = HTTPBadRequest.code
            return err.asdict()

        # Delete the Film and return 'None':
        self.context.delete()
        return None
