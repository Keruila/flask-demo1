from flask import Blueprint, request, jsonify, abort
from flask import session
from app.extensions import db
from app.models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
import re, os

auth = Blueprint("auth", __name__, url_prefix='/auth')


@auth.route("/register/", methods=["POST"])
def register():
    phone = request.json["phone"]
    username = request.json["username"]
    password = request.json["password"]
    lt = ["+", "-", "*", "/", "!", "@", "#", "$", "%",
          "^", "&", "(", ")", "~", "<", ">", "{", "}",
          "[", "]", "|", "?", "。", "，", "：", "；",
          "“", "”", "’", "‘", "`", "《", "》", " "]
    for i in lt:
        if i in username:
            return jsonify({"code": 201, "msg": "用户名含有非法字符"})

    obj = User.query.filter_by(phone=phone).first()
    obj1 = User.query.filter_by(username=username).first()

    if obj:
        return jsonify({"code": 201, "msg": "手机号已被注册"})
    if obj1:
        return jsonify({"code": 201, "msg": "用户名已被注册"})

    if re.match(r'^1(3[0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|8[0-9]|9[89])\d{8}$', phone):
        save = User(phone=phone, username=username, password=generate_password_hash(password))
        db.session.add(save)
        db.session.commit()
        return jsonify({"code": 200, "userName": username, "msg": "注册成功"})
    else:
        return jsonify({"code": 201, "msg": "请输入正确格式的手机号码"})


@auth.route("/login/", methods=["POST", "OPTIONS"])
def login():
    phone = request.json["phone"]
    password = request.json["password"]
    obj = User.query.filter_by(phone=phone).first()

    if not obj:
        return jsonify({"code": 201, "msg": "未找到该用户"})
    if check_password_hash(obj.password, password):
        # 设置session
        session["user_id"] = obj.id

        # print(session["user_id"])
        return jsonify({"code": 200, "id": obj.id, "msg": "登录成功"})
    else:
        return jsonify({"code": 400, "msg": "密码错误"})


def userinfo_replace_id_url(tasks):
    return dict(
        phone = tasks.phone,
        username=tasks.username,
        avatar_url=tasks.avatar_url
    )


# 个人中心 获取用户基本信息
@auth.route("/set_userinfo/", methods=["POST"])
def set_userinfo():
    id = session.get("user_id")
    s = User.query.filter_by(id=id).all()

    if id:
        return jsonify({"code": 200, "data": list(map(userinfo_replace_id_url, s)), "msg": "请谨慎修改信息"})
    return jsonify({"code": 201, "msg": "请先登录"})


# 修改用户名
@auth.route("/set_username/", methods=["POST"])
def set_username():
    id = session.get("user_id")
    user = User.query.get(id)
    new_username1 = request.json["username"]
    lt = ["+", "-", "*", "/", "!", "@", "#", "$", "%",
          "^", "&", "(", ")", "~", "<", ">", "{", "}",
          "[", "]", "|", "?", "。", "，", "：", "；",
          "“", "”", "’", "‘", "`", "《", "》", " "]
    for i in lt:
        if i in new_username1:
            return jsonify({"code": 201, "msg": "用户名含有非法字符"})

    new_username = User.query.filter_by(username=new_username1).first()
    if user is None:
        abort(404)
    if not request.json:
        abort(400)
    if new_username:
        return jsonify({"code": 201, "msg": "用户名重复"})

    if id:
        user = User.query.get(id)
        user.username = new_username1
        db.session.commit()
        return jsonify({"code": 200, "msg": "修改成功"})
    return jsonify({"code": 201, "msg": "先登录在来吧"})

# 修改密码
@auth.route("/set_password/", methods=["POST"])
def set_password():
    id = session.get("user_id")
    user = User.query.get(id)
    new_password = request.json["password"]
    # new_username = User.query.filter_by(password=new_username1).first()
    if user is None:
        abort(404)
    if not request.json:
        abort(400)
    if check_password_hash(user.password, new_password):
        return jsonify({"code": 201, "msg": "密码不能重复"})

    if id:
        user = User.query.get(id)
        user.password = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({"code": 200, "msg": "修改成功"})
    return jsonify({"code": 201, "msg": "先登录在来吧"})

@auth.route("/get_avatar_url/", methods=["POST"])
def get_avatar_url():
    """展示所有的头像"""
    # 先获取图片的路径
    chat_heard_path = "app/static/img/avatar/"
    img_list = os.listdir(chat_heard_path)
    if img_list:
        print(img_list)
        data = []
        for img in img_list:
            img_path = os.path.join("/static/img/avatar", img)
            data.append({"img": img_path})
        return jsonify({"code": 200, "msg": data})


@auth.route("/set_avatar_url/", methods=["POST"])
def set_avatar_url():
    """用户设置头像"""
    avatar_url = request.json["avatar_url"]
    if avatar_url is None:
        abort(404)
    if not request.json:
        abort(400)
    id = session.get("user_id")
    if id:
        user = User.query.get(id)
        user.avatar_url = avatar_url
        db.session.commit()
        return jsonify({"code": 200, "msg": "修改成功"})
    return jsonify({"code": 201, "msg": "先登录在来吧"})


# 错误的定制
@auth.errorhandler(404)
def bad_request(e):
    return jsonify({"code": 201, "error": "not found"})


@auth.errorhandler(400)
def bad_request(e):
    return jsonify({"code": 201, "error": "not json"})
