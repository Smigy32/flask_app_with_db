from flask import Flask

from config import Config as config
from .database.database import db, base


def setup_database(app):
    with app.app_context():
        @app.before_first_request
        def create_tables():
            base.metadata.create_all(db)


def init_app():
    app = Flask(__name__)

    setup_database(app)

    from .views import author_bp
    app.register_blueprint(author_bp)

    return app
