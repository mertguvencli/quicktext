from os import environ
import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration
from cachetools import TTLCache
from flask_socketio import SocketIO
from core.config import settings
from uuid import uuid4

sentry_sdk.init(
    dsn=environ.get('SENTRY_DSN'),
    integrations=[
        FlaskIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../assets',
    static_url_path='/static',
)
app.config['SECRET_KEY'] = environ.get("SECRET_KEY", str(uuid4()))
socketio = SocketIO(app)
cache = TTLCache(maxsize=settings.MAX_CACHED_ITEMS, ttl=settings.EXPIRE_CACHE)

from router import routes  # noqa F401
