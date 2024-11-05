"""
Flask main module
"""

from flask import Flask, Response

import src.models

# user defined routes
try:
    from src.data.views import data_bp
except ModuleNotFoundError:
    print("[*] Skipping for CI testing")

from src.config import Config
from src.admin.views import admin_bp
from src.core.views import core_bp
from src.errors.handlers import error_bp
from src.certs.views import cert_bp
from src.content.views import content_bp


def create_app() -> Flask:
    """
    App factory that instantiates Flask and
    returns an application object

    Returns:
        Flask: Flask app instance
    """
    application = Flask(__name__)
    app_config = Config()
    application.config.from_object(app_config)
    application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # user data blueprint
    try:
        application.register_blueprint(data_bp)
    except NameError:
        print("[*] Skipping for CI testing")

    # register blueprints
    application.register_blueprint(admin_bp)
    application.register_blueprint(core_bp)
    application.register_blueprint(error_bp)
    application.register_blueprint(cert_bp)
    application.register_blueprint(content_bp)

    # create DB tables
    with application.app_context():
        src.models.db.init_app(application)
        src.models.db.create_all()

    # additional security headers in responses
    @application.after_request
    def _(response: Response) -> Response:
        """
        Sets additional secure HTTP headers in request
        responses

        Args:
            response (Response): HTTP response
        Returns:
            Response: The response to a request
        """
        default = "default-src 'self'; "
        script = "script-src 'self' 'unsafe-inline'; "
        style = "style-src 'self' 'unsafe-inline'; "
        img = "img-src 'self' data: https:;"
        csp = default + script + style + img
        response.headers['Content-Security-Policy'] = csp
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['X-XSS-Protection'] = "1; mode=block"
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        return response

    return application
