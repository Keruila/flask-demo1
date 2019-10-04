# 接口类型：互亿无线触发短信接口，支持发送验证码短信、订单通知短信等。
# 账户注册：请通过该地址开通账户http://sms.ihuyi.com/register.html
# 注意事项：
# （1）调试期间，请用默认的模板进行测试，默认模板详见接口文档；
# （2）请使用APIID（查看APIID请登录用户中心->验证码短信->产品总览->APIID）及 APIkey来调用接口；
# （3）该代码仅供接入互亿无线短信接口参考使用，客户可根据实际需要自行编写；

from ..models.user import  User
from ..extensions import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, request, jsonify, abort
import re
import requests
import random

import redis

check_code = Blueprint("check_code", __name__)
conn_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=conn_pool)




@check_code.route("/code/", methods=["POST"])
def code():
    phone = request.json["phone"]
    if not re.match(r'^1(3[0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|8[0-9]|9[89])\d{8}$', phone):
        return jsonify({"code": 201, "msg": "请输入正确格式的手机号码"})
    u = User.query.filter_by(phone=phone).first
    if u:
        checkcode = ''
        a = str(random.randint(0, 9))
        b = str(random.randint(0, 9))
        c = str(random.randint(0, 9))
        d = str(random.randint(0, 9))
        checkcode = checkcode + a + b + c + d
        url = "http://106.ihuyi.com/webservice/sms.php?method=Submit"
        # APIID
        account = "C13334102"
        # APIkey
        password = "df931fc596c83680a65a49c4a711dac0"

        mobile = phone
        content = "您的验证码是：{}。请不要把验证码泄露给其他人。".format(checkcode)
        # 定义请求的头部
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"
        }
        # 定义请求的数据
        data = {
            "account": account,
            "password": password,
            "mobile": mobile,
            "content": content,
        }
        # 发起数据
        response = requests.post(url, headers=headers, data=data)
        # url 请求的地址
        # headers 请求头部
        # data 请求的数据
        print(response.content.decode())
        r.set(phone, checkcode, ex=120)
        return jsonify({"code": 201, "data": checkcode, "msg": "发送成功"})
    return jsonify({"code": 201, "msg": "请输入正确的手机号码"})


# 忘记密码
@check_code.route("/forget_password/", methods=["POST"])
def forget_password():
    phone = request.json["phone"]
    user = User.query.filter_by(phone=phone).first()
    checkcode = r.get(phone)
    check_code = request.json["check_code"]
    # old_password = request.json["oldpassword"]
    new_password = request.json["password"]
    new_password2 = request.json["password2"]
    if user is None:
        abort(404)
    if not request.json:
        abort(400)
    if not re.match(r'^1(3[0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|8[0-9]|9[89])\d{8}$', phone):
        return jsonify({"code": 201, "msg": "请输入正确格式的手机号码"})
    # if not check_password_hash(user.password, old_password):
    #     return jsonify({"code": 201, "msg": "旧密码输入有误"})
    if new_password != new_password2:
        return jsonify({"code": 201, "msg": "两次输入密码不一致"})
    if check_password_hash(user.password, new_password):
        return jsonify({"code": 201, "msg": "新密码和旧密码不能重复"})
    if user:
        if checkcode != None:
            if check_code == checkcode:
                user.password = generate_password_hash(new_password)
                db.session.commit()
                return jsonify({"code": 200, "msg": "修改成功"})
        return jsonify({"code": 201, "msg": "验证码已过期"})
    return jsonify({"code": 201, "msg": "请先注册"})


# 错误的定制
@check_code.errorhandler(404)
def bad_request(e):
    return jsonify({"code": 201, "error": "not found"})


@check_code.errorhandler(400)
def bad_request(e):
    return jsonify({"code": 201, "error": "not json"})
