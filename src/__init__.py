from flask import Flask
import os
from src.images import images
from src.database import db

def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY")
            )
    
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)
    app.register_blueprint(images)

    return app