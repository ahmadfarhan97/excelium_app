import flask
from flask_session import Session
# from flask_caching import Cache

from . import app_config

app = flask.Flask(__name__)
app.secret_key = "password test"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config.from_object(app_config)
Session(app)

# cache = Cache(app, config={'CACHE_TYPE': app_config.SESSION_TYPE, 'CACHE_DIR': '/tmp'})