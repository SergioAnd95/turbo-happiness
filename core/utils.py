import importlib

from aiohttp import web

from settings.settings import INSTALLED_APPS

def discover_app_models():
    for app in INSTALLED_APPS:
        importlib.import_module('%s.models' % app)

def discover_app_views():
    for app in INSTALLED_APPS:
        importlib.import_module('%s.views' % app)

def redirect(request, view_name):
    location = request.app.router[view_name].url_for()
    raise web.HTTPFound(location=location)