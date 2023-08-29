import datetime
import uuid
from flask import Flask, request
import app.db.classes as Data
import app.db as db
from .api import like_api_bp,post_api_bp,login_api_bp,logout_api_bp,report_api_bp,search_user_api_bp,register_api_bp,image_post_api_bp,admin_auth_api_bp,admin_user_api_bp,user_details_api_bp,profile_image_api_bp,reset_password_api_bp,profile_details_api_bp,admin_user_list_api_bp
from .views import root_bp,register_bp ,edit_profile_bp,visit_user_bp ,reset_password_bp ,confirm_email_bp ,search_bp ,admin_login_bp ,log_bp,chat_bp
import logging
import os
from flask_cors import CORS
from .api import socketio


app = Flask(__name__)
app.config.from_pyfile('appconfig.py')

CORS(app, supports_credentials=True)

with app.app_context():
    Data.db.init_app(app)
    Data.db.create_all()
    Data.migrate.init_app(app, Data.db)
    username = app.config['ADMIN_USERNAME']
    password = app.config["ADMIN_PASSWORD"]
    email = app.config["ADMIN_EMAIL"]
    db.create_admin(username=username,password=password,email=email)



# register blueprints for each module
# root view
app.register_blueprint(root_bp)
app.register_blueprint(login_api_bp)
app.register_blueprint(logout_api_bp)
app.register_blueprint(post_api_bp)
app.register_blueprint(image_post_api_bp)
app.register_blueprint(like_api_bp)

# register view
app.register_blueprint(register_bp)
app.register_blueprint(register_api_bp)

# profile edit view
app.register_blueprint(edit_profile_bp)
app.register_blueprint(profile_details_api_bp)
app.register_blueprint(profile_image_api_bp)
app.register_blueprint(user_details_api_bp)

# password reset view
app.register_blueprint(reset_password_bp)
app.register_blueprint(reset_password_api_bp)


# visit user view
app.register_blueprint(visit_user_bp)

# confirm email view
app.register_blueprint(confirm_email_bp)

# search view
app.register_blueprint(search_bp)
app.register_blueprint(search_user_api_bp)

# admin login view
app.register_blueprint(admin_login_bp)
app.register_blueprint(admin_auth_api_bp)
app.register_blueprint(admin_user_list_api_bp)
app.register_blueprint(admin_user_api_bp)


# log view
app.register_blueprint(log_bp)
app.register_blueprint(report_api_bp)

# chat view
app.register_blueprint(chat_bp)
with app.app_context():
   socketio.init_app(app)




logging.basicConfig(filename=os.path.join(app.root_path,'record.log'), level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

@app.before_request
def log_request_info():
    if not "/static" in request.full_path:
        app.logger.debug('Method: %s %s', request.method, request.full_path)
        app.logger.debug('User-Agent: %s', request.headers.get('User-Agent'))
        ip = request.headers.get('X-REAL-IP')
        if not ip:
            ip = request.headers.get('X-FORWARDED-FOR')
        if not ip:
            ip = request.headers.get('RemoteAddr')
        app.logger.debug('IP: %s', ip)
        app.logger.debug('Data: %s', request.get_data())
        app.logger.debug('Date: %s', datetime.datetime.now())
        
        
        