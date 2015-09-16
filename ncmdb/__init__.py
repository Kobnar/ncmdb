from pyramid.config import Configurator
from pyramid.renderers import JSON
from sqlalchemy import engine_from_config

from .resources import RootResource, PersonRowResource, PersonTableResource
from .models import DBSession, Base


def traversal_factory(request):
    root = RootResource(None, '')
    root['api'] = RootResource
    root['api']['v1'] = RootResource
    root['api']['v1']['people'] = PersonTableResource
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
    config.add_renderer('json', JSON(indent=4))
    config.scan()
    return config.make_wsgi_app()
