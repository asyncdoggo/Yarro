import glob
import os
import flask
from flask import request, send_from_directory
from werkzeug.utils import secure_filename
from app.api.token_required import token_required
from flask_restful import Resource
from PIL import Image



class ProfileImage(Resource):
    def get(self, path):
        uid = secure_filename(path)
        image_path = glob.glob(os.path.join(flask.current_app.root_path, "static", "userimages", f"{path}.*"))
        image_file = image_path[0].split(os.sep)[-1] if image_path else "default.png"
        image_folder = os.path.join(flask.current_app.root_path, "static", "userimages")
        return send_from_directory(image_folder, image_file)

    @token_required
    def post(self, user):
        try:
            file = request.files["image"]
            img = Image.open(file.stream)
            image_type = file.mimetype.split("/")[1]
            filename = secure_filename(f"{user.id}.{image_type}")
            img.save(os.path.join(flask.current_app.root_path, "static", "userimages", filename), optimize=True, quality=90)
            return {"status": "success"}
        except KeyError as e:
            print(e)
            return {"status": "failure"}
