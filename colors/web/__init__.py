from os import environ
from os.path import abspath
import urlparse

from flask import Flask

from colors.controller import ColorsController

app = None
controller = None

def build_app(
    static_folder=None,
    static_url_path=None,
    template_folder=None,
    secret_key=None):

    global app, controller

    mq_url = environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')
    url = urlparse.urlparse(mq_url)
    mongo_uri = environ.get('MONGOHQ_URL', 'mongodb://localhost:27017/colors')
    database = urlparse.urlparse(mongo_uri).path[1:]

    controller = ColorsController(host=url.hostname, virtual_host=url.path[1:], username=url.username, password=url.password, mongo_uri=mongo_uri, database=database)

    params = dict()

    if static_folder:
        params['static_folder'] = abspath(static_folder)

    if static_url_path:
        params['static_url_path'] = abspath(static_url_path)

    if template_folder:
        params['template_folder'] = abspath(template_folder)

    app = Flask(__name__, **params)

    if secret_key is None:
        secret_key = 'development'

    app.secret_key = secret_key

    import colors.web.views

    return app
