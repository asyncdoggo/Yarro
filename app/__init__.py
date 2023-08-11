from flask import Flask, request,current_app
import app.db.classes as Data
from .api import api_bp
from .views import view_bp
import logging
import os
from flask_cors import CORS
from .api import socketio


app = Flask(__name__)
app.config.from_pyfile('appconfig.py')

CORS(app)
with app.app_context():
    Data.db.init_app(app)
    Data.db.create_all()
    Data.migrate.init_app(app, Data.db)
    socketio.init_app(app)



app.register_blueprint(view_bp)
app.register_blueprint(api_bp)

logging.basicConfig(filename=os.path.join(app.root_path,'record.log'), level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')



@app.before_request
def log_request_info():
    app.logger.debug('User-Agent: %s', request.headers.get('User-Agent'))
    ip = request.headers.get('X-REAL-IP')
    if not ip:
       ip = request.headers.get('X-FORWARDED-FOR')
    if not ip:
       ip = request.headers.get('RemoteAddr')
    

    app.logger.debug('IP: %s', ip)
    app.logger.debug('Data: %s', request.get_data())