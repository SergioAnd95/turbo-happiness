from gino import Gino

from settings import settings
from .utils import discover_app_models

db = Gino()

discover_app_models()
