import bfly.job_match.api
import bfly.jobs.api
import bfly.majors.api
import bfly.users.api
import bfly.db
import bfly.server
import flask
import flask_bootstrap
import logging


def create_app(config, debug=False, testing=False):

    app = flask.Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    # Setup the data model.
    with app.app_context():
        # I hate this and need to figure out how to not have the db as a context of things.
        bfly.db.init_app(app)

    # Register our apis
    # app.register_blueprint(bfly.job_match.api.job_match)
    app.register_blueprint(bfly.jobs.api.jobs)
    app.register_blueprint(bfly.majors.api.majors)
    app.register_blueprint(bfly.users.api.users, url_prefix='/users')
    app.register_blueprint(bfly.job_match.api.job_match, url_prefix='/job_match')
    flask_bootstrap.Bootstrap(app)
    from bfly.users import models
    # Add an error handler. This is useful for debugging the live application,
    # however, you should disable the output of the exception for production
    # applications.
    @app.errorhandler(500)
    def server_error(e):
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    return app
