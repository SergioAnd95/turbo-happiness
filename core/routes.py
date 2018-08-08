from aiohttp import web

from .utils import discover_app_views

routes = web.RouteTableDef()

discover_app_views()