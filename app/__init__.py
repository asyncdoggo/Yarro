from flask import Flask
import app.Database as Data
from app.api import api_bp
from app.views import view_bp

app = Flask(__name__)

app.config.from_pyfile('appconfig.py')

with app.app_context():
    Data.db.init_app(app)
    Data.db.create_all()

app.register_blueprint(view_bp)
app.register_blueprint(api_bp)
