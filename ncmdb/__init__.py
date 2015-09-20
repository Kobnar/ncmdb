from pyramid.config import Configurator
from pyramid.renderers import JSON
from sqlalchemy import engine_from_config

from .resources import IndexResource, PersonTableResource, FilmTableResource
from .models import DBSession, Base


def traversal_factory(request):
    root = IndexResource(None, '')
    root['api'] = IndexResource
    root['api']['v1'] = IndexResource
    root['api']['v1']['people'] = PersonTableResource
    root['api']['v1']['films'] = FilmTableResource
    return root


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings,
                          root_factory=traversal_factory)
    config.include('pyramid_jinja2')
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    template_path = settings['jinja2_template_path']
    config.add_jinja2_search_path(template_path)
    config.add_renderer('json', JSON(indent=4))
    config.scan()
    return config.make_wsgi_app()
