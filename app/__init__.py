from flask import Flask
import app.db.classes as Data
from app.api import api_bp
from app.views import view_bp

app = Flask(__name__)
app.config.from_pyfile('appconfig.py')

with app.app_context():
    Data.db.init_app(app)
    Data.db.create_all()
    Data.migrate.init_app(app, Data.db)

app.register_blueprint(view_bp)
app.register_blueprint(api_bp)
