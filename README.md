# Yarro
Yarro is a social networking website made in flask
## Try it out
[https://yarro.onrender.com](https://yarro.onrender.com)

# Run locally

## Requirements
- python 3.6+
- mysql server (optional)

## Usage
- clone the repo
```
git clone https://github.com/asyncdoggo/Yarro.git
```
- install requirements using pip
```
python -m pip install -r requirements.txt
```

- create a file with name `.env` in the project root with following variables
```
# database engine to be used, currently supported (mysql, sqlite)
DB_ENGINE = sqlite

# jwt secret
SECRET_KEY=super-secret-key


# email secrets
EMAIL=email@example.com
EMAIL_PASSWORD=password

# Database connection parameters
# set all to blank if using sqlite
HOST=localhost
USERNAME=example
PASSWORD=password
DATABASE=yarrodb
```

- open http://localhost:3000
host and port can be changed in run.py


