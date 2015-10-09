import inspect
import logging
import logging.handlers
from flask import Flask
from flask.ext.babel import Babel
from flask.ext.mongoengine import MongoEngine

from project.config import MainConfig
from project.extensions import cache

__all__ = ['init_app']


def init_app(config, app_name):
    """
    main function for initializing all
    """

    app = Flask(
        app_name
    )

    configure(app, config)
    installing_blueprints(app)
    il8n(app)
    connect_db(app)
    logger(app)
    template_tags(app)
    extensions(app)

    return app


def configure(app, config):
    """
    Loading app config
    """
    app.config.from_object(MainConfig())
    if config:
        app.config.from_object(config)


def installing_blueprints(app):
    """
    registering blueprints and importing from views
    """

    app.config.setdefault('APPS_LIST', [])
    apps_list = app.config['APPS_LIST']

    for controller in apps_list:
        bp = __import__('project.apps.%s' % controller, fromlist=['views'])
        try:
            app.register_blueprint(bp.views.mod)
        except:
            pass


def il8n(app):
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        pass


def connect_db(app):
    MongoEngine(app)


def logger(app):
    """
    This function Configure Logger for given Application.

    :param app: Application Object
    :type app: Object
    """

    # from project.utils.extended_logging import wrap_app_logger
    # wrap_app_logger(app)
    if app.debug or app.testing:
        from project.utils.extended_logging import wrap_app_logger
        wrap_app_logger(app)
        app.logger.create_logger('debuging')
        return

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')

    debug_file_handler = logging.handlers.RotatingFileHandler(
        app.config['DEBUG_LOG'],
        maxBytes=100000,
        backupCount=10)

    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)

    error_file_handler = logging.handlers.RotatingFileHandler(
        app.config['ERROR_LOG'],
        maxBytes=100000,
        backupCount=10)

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)


def template_tags(app):
    import project.utils.template_tags as temp_tags
    tags = inspect.getmembers(temp_tags, inspect.isfunction)
    for tag in tags:
        app.jinja_env.globals[tag[0]] = tag[1]


def extensions(app):
    cache.init_app(app)
