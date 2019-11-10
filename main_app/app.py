from flask import Flask


def create_app(settings_override=None):

    """
    Create a Flask application using the app factory pattern.

    :return: Flask app
    """

    from main_app.blueprints.pages.views import page
    from main_app.blueprints.apiv1 import api_blueprint

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    from main_app.blueprints.apiv1 import limiter
    limiter.init_app(app)

    app.register_blueprint(page)
    app.register_blueprint(api_blueprint)

    return app


flask_app = create_app()


