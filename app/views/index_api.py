from flask import Blueprint, request, jsonify

import os

index = Blueprint("index", __name__)


@index.route("/rotation/", methods=["GET"])
def rotation_chart():
    rotation_path = "app/static/img/rotation/"
    img_list = os.listdir(rotation_path)
    if img_list:
        data = []
        for img in img_list:
            img_path = os.path.join("/static/img/rotation/", img)
            data.append({"img": img_path})
        result = {
            "code": 200,
            "msg": "请求成功",
            "data": data
        }
        return jsonify(result)
    else:
        result = {
            "code": 204,
            "msg": "没有数据可返回",
            "data": []
        }
        return jsonify(result)
