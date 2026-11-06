from . import app
import os
import json
from flask import jsonify, request

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
with open(json_url, encoding="utf-8") as picture_file:
    data: list = json.load(picture_file)


@app.route("/health")
def health():
    return jsonify({"status": "OK"}), 200


@app.route("/count")
def count():
    return jsonify(length=len(data)), 200


@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return jsonify(picture), 200
    return jsonify({"message": "picture not found"}), 404


@app.route("/picture", methods=["POST"])
def create_picture():
    picture_in = request.get_json(silent=True)
    if not isinstance(picture_in, dict) or "id" not in picture_in:
        return jsonify({"message": "invalid picture payload"}), 400
    for picture in data:
        if picture_in["id"] == picture["id"]:
            return jsonify({"Message": f"picture with id {picture_in['id']} already present"}), 302
    data.append(picture_in)
    return jsonify(picture_in), 201


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture_in = request.get_json(silent=True)
    if not isinstance(picture_in, dict):
        return jsonify({"message": "invalid picture payload"}), 400
    for index, picture in enumerate(data):
        if picture["id"] == id:
            data[index] = picture_in
            return jsonify(picture_in), 201
    return jsonify({"message": "picture not found"}), 404


@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for picture in data:
        if picture["id"] == id:
            data.remove(picture)
            return "", 204
    return jsonify({"message": "picture not found"}), 404
