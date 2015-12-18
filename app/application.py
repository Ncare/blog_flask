from flask import Flask

from app.database import db

from app.views.web import fp
from app.views.admin import bp



DEFAULT_APP_NAME = 'app'


def create_app():
    app = Flask(DEFAULT_APP_NAME)
    app.config.from_object('config')

    db.init_app(app)
    with app.test_request_context():
        from app.models import User,Post, Comment
        db.create_all()

    app.register_blueprint(fp, url_prefix='')
    app.register_blueprint(bp, url_prefix='/admin')

    return app



