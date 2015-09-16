from pyramid.view import view_defaults, view_config
from pyramid.exceptions import HTTPNotFound

from .resources import PersonTableResource


class BaseView(object):
    """
    Provides a default view configuration for common view elements and output.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request


@view_defaults(context=PersonTableResource, renderer='json')
class PersonIndexAPIViews(BaseView):
    @view_config(request_method='GET')
    def retrieve(self):
        query = self.request.params
        result = self.context.retrieve(query)
        output = []
        for person in result:
            output.append({
                'id': person.id,
                'name': person.name,
                'img_uri': person.img_uri,
                'producer_credits': person.producer_credits,
                'director_credits': person.director_credits,
                'writer_credits': person.writer_credits,
                'editor_credits': person.editor_credits,
                'cast_credits': person.cast_credits,
                'musician_credits': person.musician_credits})
        if not output:
            self.request.response.status_int = HTTPNotFound.code
        return output
