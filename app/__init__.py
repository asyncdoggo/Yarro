from flask import Flask, Blueprint
from flask_restful import Api
import app.Database as Data
from app.views import view_bp
from app.api import api_bp

app = Flask(__name__)

app.config.from_pyfile('appconfig.py')

with app.app_context():
    Data.db.init_app(app)
    Data.db.create_all()

# blueprints for blogs & users
app.register_blueprint(view_bp)
app.register_blueprint(api_bp)
