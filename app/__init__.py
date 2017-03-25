import os
from flask import Flask
from flask_moment import Moment
from flask_flatpages import FlatPages
from flask_frozen import Freezer

from werkzeug.contrib.fixers import ProxyFix

from config import config, basedir

from . htmlabbrev import HTMLAbbrev

moment = Moment()
pages = FlatPages()
freezer = Freezer()


def htmltruncate(value, maxlen=150):
    parser = HTMLAbbrev(maxlen)
    parser.feed(value)
    return parser.close()


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    moment.init_app(app)
    pages.init_app(app)
    freezer.init_app(app)

    from . main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from . blog import blog as blog_blueprint
    app.register_blueprint(blog_blueprint, url_prefix='/blog')

    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.jinja_env.filters['htmltruncate'] = htmltruncate

    if not os.path.exists(os.path.join(basedir, 'tmp')):
        os.makedirs(os.path.join(basedir, 'tmp'))

    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler

        file_handler = RotatingFileHandler('tmp/healy.log', 'a',
                                           1 * 1024 * 1024, 10)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %(message)s ' +
                              '[in %(pathname)s:%(lineno)d]'))
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('app startup')

    return app
