from flask import Blueprint, request, jsonify
import re
from flask import session
from app.extensions import db
from app.models.user import User
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint("auth", __name__, url_prefix='/auth')


@auth.route("/register/", methods=["POST"])
def register():
    phone = request.form["phone"]
    username = request.form["username"]
    password = request.form["password"]

    obj = User.query.filter_by(phone=phone).first()

    if obj:
        return jsonify({"code": 201, "msg": "用户名已被注册"})

    if re.match(r'^1[345789]\d{9}$', phone):
        save = User(phone=phone, username=username, password=generate_password_hash(password))
        db.session.add(save)
        db.session.commit()
        return jsonify({"code": 200, "userName": username, "msg": "注册成功"})
    else:
        return jsonify({"code": 301, "msg": "请输入正确手机号码"})


@auth.route("/login/", methods=["POST"])
def login():
    phone = request.form["phone"]
    password = request.form["password"]
    obj = User.query.filter_by(phone=phone).first()

    if not obj:
        return jsonify({"code": 201, "msg": "未找到该用户"})
    if check_password_hash(obj.password, password):
        # 设置session
        session["user_id"] = obj.id
        return jsonify({"code": 200, "id": obj.id, "msg": "登录成功"})
    else:
        return jsonify({"code": 400, "msg": "密码错误"})
