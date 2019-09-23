from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint("auth", __name__, url_prefix='/auth')


@auth.route("/")
def index():
    return "我是新来的用户"


@auth.route("/register/", methods=["POST"])
def register():
    phone = request.form["phone"]
    username = request.form["username"]
    password = request.form["password"]

    obj = User.query.filter_by(phone=phone).first()

    if obj:
        return jsonify({"code": 201, "msg": "用户名已被注册"})

    if len(list(map(int, str(phone)))) == 11:
        save = User(phone=phone, username=username, password=password)
        db.session.add(save)
        db.session.commit()
        return jsonify({"code": 1, "userName": username, "msg": "注册成功"})
    else:
        return jsonify({"code": 201, "msg": "请输入正确手机号码"})


@auth.route("/login/", methods=["POST"])
def login():
    phone = request.form["phone"]
    password = request.form["password"]
    obj = User.query.filter_by(phone=phone).first()
    print(obj, type(obj))
    if not obj:
        return jsonify({"code": 201, "msg": "未找到该用户"})
    if password == obj.password:
        return jsonify({"code": 200, "msg": "登录成功"})
    else:
        return jsonify({"code": 200, "msg": "密码错误"})
