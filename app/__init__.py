import os
from flask import Flask
from flask_smorest import Api

from dotenv import load_dotenv
from app.db import init_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)

    # config mapping ...
    app.config.setdefault("DATABASE_URL", DATABASE_URL)
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    app.config.setdefault("TESTING", False)

    app.config["API_TITLE"] = "Task Manager API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_REDOC_PATH"] = "/docs"     # ReDoc
    app.config["OPENAPI_REDOC_URL"] = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger"  # Swagger UI
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/"

    app.config["API_SPEC_OPTIONS"] = {
        "security": [{"bearerAuth": []}],
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        }
    }

    if config:
        app.config.update(config)

    init_engine(app.config["DATABASE_URL"], echo=False, future=True)

    api = Api(app)

    # register Blueprints
    from app.tasks.routes import blp as tasks_bp

    api.register_blueprint(tasks_bp)

    from app.auth.routes import blp as auth_bp

    api.register_blueprint(auth_bp)

    return app
