from dotenv import dotenv_values
import os
config = dotenv_values(".env")

HOST = config["HOST"]
USERNAME = config["USERNAME"]
PASSWORD = config["PASSWORD"]
DATABASE = config["DATABASE"]

SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = False
SQLALCHEMY_DATABASE_URI = ""

if config["DB_ENGINE"] == "mysql":
    SQLALCHEMY_DATABASE_URI = f'mysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}?ssl=true'

elif config["DB_ENGINE"] == "sqlite":
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.getcwd()}/data.db"


SECRET_KEY = config["SECRET_KEY"]


ADMIN_USERNAME = config["ADMIN_USERNAME"]
ADMIN_PASSWORD = config["ADMIN_PASSWORD"]
ADMIN_EMAIL = config["ADMIN_EMAIL"]
