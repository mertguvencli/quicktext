
from os import environ
from flask import Flask
from cachetools import TTLCache
from flask_socketio import SocketIO
from core.config import settings
from uuid import uuid4


app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../assets',
    static_url_path='/static',
)
app.config['SECRET_KEY'] = environ.get("secret-key", str(uuid4()))
socketio = SocketIO(app)
cache = TTLCache(maxsize=settings.MAX_CACHED_ITEMS, ttl=settings.EXPIRE_CACHE)

from router import routes  # noqa F401
