from dotenv import dotenv_values

config = dotenv_values(".env")

HOST=config["HOST"]
USERNAME=config["USERNAME"]
PASSWORD=config["PASSWORD"]
DATABASE=config["DATABASE"]

SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = False
SQLALCHEMY_DATABASE_URI = f'mysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}?ssl=true'
SECRET_KEY = config["SECRET_KEY"]