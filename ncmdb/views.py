from pyramid.view import view_defaults, view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPCreated, HTTPBadRequest
from colander import Invalid

from .resources import PersonTableResource, PersonRowResource
from .schema import IdSchema, CreatePersonRowSchema, UpdatePersonRowSchema,\
    RetrievePersonRowSchema


class BaseView(object):
    """
    Provides a default view configuration for common view elements and output.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request


@view_defaults(context=PersonTableResource, renderer='json')
class PeopleAPIIndexViews(BaseView):
    """/api/v1/people/
    """

    @view_config(request_method='POST')
    def create(self):
        schema = CreatePersonRowSchema()
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
        schema = UpdatePersonRowSchema()
        try:
            data = schema.deserialize(self.request.GET)
        except Invalid as err:
            self.request.response.status_int = HTTPBadRequest.code
            return err.asdict()
        result = self.context.retrieve(data)
        output = [x.serialized for x in result]
        if not output:
            self.request.response.status_int = HTTPNotFound.code
        return output


@view_defaults(context=PersonRowResource, renderer='json')
class PersonAPIViews(BaseView):
    """/api/v1/people/{#}/
    """

    @view_config(request_method='GET')
    def retrieve(self):
        id_schema = IdSchema()
        fields_schema = RetrievePersonRowSchema()
        try:
            id_schema.deserialize({'id': self.context.id})
            data = fields_schema.deserialize(self.request.GET)
        except Invalid as err:
            self.request.response.status_int = HTTPBadRequest.code
            return err.asdict()
        result = self.context.retrieve()
        if result:
            result = result.serialized
            print(result)
            if data['fields']:
                result = {k: v for k, v in result.items()
                          if k in data['fields']}
            return result
        self.request.response.status_int = HTTPNotFound.code
        return {}

    @view_config(request_method='PUT')
    def update(self):
        id_schema = IdSchema()
        row_schema = UpdatePersonRowSchema()
        try:
            id_schema.deserialize({'id': self.context.id})
            data = row_schema.deserialize(self.request.POST)
        except Invalid as err:
            self.request.response.status_int = HTTPBadRequest.code
            return err.asdict()
        result = self.context.update(data)
        if result:
            return result.serialized
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
