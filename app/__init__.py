from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import config_by_name

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from app.main.views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.notes.views import notes as notes_blueprint
    app.register_blueprint(notes_blueprint, url_prefix='/notes')

    return app
