import glob
import os
import uuid
import flask
from flask import request, send_from_directory
from werkzeug.utils import secure_filename
import app.db as Data
from app.api.token_required import token_required
from flask_restful import Resource
from PIL import Image

class ImagePost(Resource):
    @token_required
    def get(self, _, path):
        path = secure_filename(path)
        image_path = glob.glob(os.path.join(flask.current_app.root_path, "static", "images", path))
        image_file = image_path[0].split(os.sep)[-1] if image_path else "not_available.png"
        image_folder = os.path.join(flask.current_app.root_path, "static", "images")
        return send_from_directory(image_folder, image_file)

    @token_required
    def post(self, user):
        file = request.files["image"]
        img = Image.open(file.stream)
        image_type = file.mimetype.split("/")[1]
        filename = secure_filename(f"{uuid.uuid4().hex}.{image_type}")
        if Data.insert_post_image(user, filename):
            img.save(os.path.join(flask.current_app.root_path, "static", "images", filename), optimize=True, quality=90)
            return {"status": "success"}
        return {"status": "failure"}

