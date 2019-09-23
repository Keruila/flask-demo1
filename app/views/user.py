from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User

user = Blueprint("user", __name__)


@user.route("/")
def index():
    return "我是新来的用户"


@user.route("/user/register/", methods=["POST"])
def register():
    phone = request.json["phone"]
    username = request.json["username"]
    password = request.json["password"]
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


@user.route("/user/login/", methods=["POST"])
def login():
    phone = request.json["phone"]
    password = request.json["password"]
    obj = User.query.filter_by(phone=phone).first()
    print(obj, type(obj))
    if not obj:
        return jsonify({"code": 201, "msg": "未找到该用户"})
    if password == obj.password:
        return jsonify({"code": 200, "msg": "登录成功"})
    else:
        return jsonify({"code": 200, "msg": "密码错误"})
