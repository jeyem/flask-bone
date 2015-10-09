from flask.ext.cache import Cache
from flask.ext.session import Session

__all__ = ['cache']

cache = Cache()
session = Session()
