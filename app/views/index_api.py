from flask import Blueprint, request, jsonify

import os

index = Blueprint("index", __name__)


@index.route("/rotation/", methods=["GET"])
def rotation_chart():
    result = {
        "code": 200,
        "data": [
            {"img": "/static/img/rotation/HA-1001.png"},
            {"img": "/static/img/rotation/HA-1039.png"},
            {"img": "/static/img/rotation/HA-1103.png"},
        ]
    }
    return jsonify(result)
