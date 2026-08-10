from flask import Flask
from flasgger import Swagger

from api.response import error_json


SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "eGemWallet API",
        "description": "Flask API sa slojevima API -> BLL -> DAL -> SQL Server SP.",
        "version": "1.0.0",
    },
    "basePath": "/",
    "schemes": ["http"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
}

SWAGGER_CONFIG = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
}


def create_app():
    app = Flask(__name__)

    Swagger(app, template=SWAGGER_TEMPLATE, config=SWAGGER_CONFIG)

    register_blueprints(app)
    register_error_handlers(app)

    @app.route("/health", methods=["GET"])
    def health():
        """Health check
        ---
        tags:
          - System
        responses:
          200:
            description: Service is up
        """
        return {"status": "ok"}

    return app


def register_blueprints(app):
    from api.endpoints.register_user_endpoints import register_user_bp
    from api.endpoints.link_identity_endpoints import link_identity_bp
    from api.endpoints.get_balance_endpoints import get_balance_bp
    from api.endpoints.put_amount_endpoints import put_amount_bp

    app.register_blueprint(register_user_bp, url_prefix="/api/user")
    app.register_blueprint(link_identity_bp, url_prefix="/api/user")
    app.register_blueprint(get_balance_bp, url_prefix="/api/wallet")
    app.register_blueprint(put_amount_bp, url_prefix="/api/wallet")


def register_error_handlers(app):
    from werkzeug.exceptions import HTTPException

    @app.errorhandler(HTTPException)
    def handle_http_error(e):
        return error_json(e.description or str(e), e.code or 500)

    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        # pymssql exceptions imaju args = (error_code, b'SQL Server message')
        args = getattr(e, "args", ()) or ()
        if len(args) >= 2:
            raw = args[1]
            if isinstance(raw, bytes):
                return error_json(raw.decode("utf-8", errors="ignore").strip(), 500)
            if isinstance(raw, str):
                return error_json(raw.strip(), 500)
        return error_json(f"{type(e).__name__}: {e}", 500)
