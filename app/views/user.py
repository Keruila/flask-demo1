from flask import Blueprint, request, jsonify, abort
from flask import session
from app.extensions import db
from app.models.user import User, Collect
from werkzeug.security import check_password_hash, generate_password_hash
import re, os

auth = Blueprint("auth", __name__, url_prefix='/auth')


@auth.route("/register/", methods=["POST"])
def register():
    phone = request.json["phone"]
    username = request.json["username"]
    password = request.json["password"]
    obj = User.query.filter_by(phone=phone).first()
    obj1 = User.query.filter_by(username=username).first()
    lt = ["+", "-", "*", "/", "!", "@", "#", "$", "%",
          "^", "&", "(", ")", "~", "<", ">", "{", "}",
          "[", "]", "|", "?", "。", "，", "：", "；",
          "“", "”", "’", "‘", "`", "《", "》", " "]
    if obj:
        return jsonify({"code": 201, "msg": "手机号已被注册"})
    if obj1:
        return jsonify({"code": 201, "msg": "用户名已被注册"})

    for i in lt:
        if i in username:
            return jsonify({"code": 201, "msg": "用户名含有非法字符"})

    if re.match(r'^1(3[0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|8[0-9]|9[89])\d{8}$', phone):
        save = User(phone=phone, username=username, password=generate_password_hash(password))
        db.session.add(save)
        db.session.commit()
        return jsonify({"code": 200, "userName": username, "msg": "注册成功"})
    else:
        return jsonify({"code": 201, "msg": "请输入正确格式的手机号码"})


@auth.route("/login/", methods=["POST"])
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
        phone=tasks.phone,
        username=tasks.username,
        avatar_url=tasks.avatar_url
    )


# 个人中心 获取用户基本信息
@auth.route("/set_userinfo/", methods=["POST"])
def set_userinfo():
    id = request.json["user_id"]
    # id = session.get("user_id")
    s = User.query.filter_by(id=id).all()

    if id:
        return jsonify({"code": 200, "data": list(map(userinfo_replace_id_url, s)), "msg": "请谨慎修改信息"})
    return jsonify({"code": 201, "msg": "请先登录"})


# 修改用户名
@auth.route("/set_username/", methods=["POST"])
def set_username():
    id = request.json["user_id"]
    # id = session.get("user_id")
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
    id = request.json["user_id"]
    # id = session.get("user_id")
    user = User.query.get(id)
    old_password = request.json["oldpassword"]
    new_password = request.json["password"]
    new_password2 = request.json["password2"]
    # new_username = User.query.filter_by(password=new_username1).first()
    if user is None:
        abort(404)
    if not request.json:
        abort(400)
    if not check_password_hash(user.password, old_password):
        return jsonify({"code": 201, "msg": "旧密码输入有误"})
    if new_password != new_password2:
        return jsonify({"code":201, "msg":"两次输入密码不一致"})
    if check_password_hash(user.password, new_password):
        return jsonify({"code": 201, "msg": "密码不能与旧密码相同"})

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
    id = request.json["user_id"]
    # id = session.get("user_id")
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


@auth.route('/profile/', methods=["POST"])
def profile():
    user_id = request.json['user_id']
    # user_id = session.get("id")
    user = User.query.filter_by(id=user_id).first()
    if not user:
        result = {
            'code': 201,
            'msg': '用户不存在',
            "data": {}
        }
        return jsonify(result)
    user_profile = dict(
        id=user.id,
        username=user.username,
        phone=user.phone
    )
    result = {
        'code': 200,
        'msg': '请求成功',
        "data": user_profile
    }
    return jsonify(result)


@auth.route('/add_collect/', methods=["POST"])
def add_collect():
    """加入收藏"""
    user_id = request.json['user_id']
    door_id = request.json['door_id']
    if not user_id or not door_id:
        result = {
            'code': 204,
            'msg': '缺失用户id或商品id'
        }
        return jsonify(result)
    collect = Collect(user_id=user_id, door_id=door_id)
    db.session.add(collect)
    db.session.commit()
    result = {
        'code': 200,
        'msg': '收藏成功'
    }
    return jsonify(result)


@auth.route('/cancel_collect/', methods=['POST'])
def cancel_collect():
    """取消收藏"""
    user_id = request.json['user_id']
    door_id = request.json['door_id']
    if not user_id or not door_id:
        result = {
            'code': 204,
            'msg': '缺失用户id或商品id'
        }
        return jsonify(result)
    collect = Collect.query.filter_by(user_id=user_id, door_id=door_id).first()
    db.session.delete(collect)
    db.session.commit()
    result = {
        'code': 200,
        'msg': '取消收藏成功'
    }
    return jsonify(result)


@auth.route('/all_collect/', methods=['POST'])
def all_collect():
    """所有收藏"""
    user_id = request.json['user_id']
    collects = Collect.query.filter_by(user_id=user_id).all()  # list
    print(collects, type(collects))
    if not collects:
        result = {
            'code': 203,
            'msg': '某得收藏',
            'data': []
        }
        return jsonify(result)
    data = [collect.door_id for collect in collects]
    result = {
        'code': 200,
        'msg': 'id为{}的用户收藏的所有商品的id返回成功'.format(user_id),
        'data': data
    }
    return jsonify(result)
