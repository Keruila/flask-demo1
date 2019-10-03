from flask import Blueprint, request, jsonify, abort, session
from flask import session
from app.extensions import db
from app.models.user import ShoppingCart, User, Door
# from werkzeug.security import check_password_hash, generate_password_hash
import re, os

shopping = Blueprint("shopping", __name__, url_prefix='/shopping')


# 加入购物车
@shopping.route("/add_shopping_cart/", methods=["POST"])
def add_shopping_cart():
    user_id = request.json["user_id"]
    door_id = request.json["door_id"]
    u = ShoppingCart.query.filter_by(user_id=user_id,door_id=door_id).first()

    # u.door_id = ShoppingCart.query.filter_by(door_id=door_id).first()
    if not user_id:
        result = {
            "code": 204,
            "msg": "请先登录"
        }
        return jsonify(result)
    if not door_id:
        result = {
            "code": 204,
            "msg": "缺少产品id"
        }
        return jsonify(result)
    if u :
        u.number += 1
        db.session.commit()
        return jsonify({"code": 200, "msg": "加入购物车成功"})
    save = ShoppingCart(user_id=user_id, door_id=door_id)
    db.session.add(save)
    db.session.commit()
    return jsonify({"code": 200, "msg": "加入购物车成功"})


# 在购物车中已存在的商品的数量 -1
@shopping.route("/reduce_shopping_cart/", methods=["POST"])
def reduce_shopping_cart():

    user_id = request.json["user_id"]
    door_id = request.json["door_id"]
    u = ShoppingCart.query.filter_by(user_id=user_id,door_id=door_id).first()

    if not user_id:
        result = {
            "code": 204,
            "msg": "请先登录"
        }
        return jsonify(result)
    if not door_id:
        result = {
            "code": 204,
            "msg": "缺少产品id"
        }
        return jsonify(result)
    if u:
        if u.number == 1:
            db.session.commit()

            return jsonify({"code":200, "msg": "数量操作成功"})
        u.number -= 1
        db.session.commit()
        return jsonify({"code": 200, "msg": "数量操作成功"})
    return jsonify({"code":204, "msg":"数据错误"})
# 在购物车中删除一个记录
@shopping.route("/delete_shopping_cart/", methods=["POST"])
def delete_shopping():
    user_id = request.json["user_id"]
    door_id = request.json["door_id"]
    u = ShoppingCart.query.filter_by(user_id=user_id).first()
    d = ShoppingCart.query.filter_by(door_id=door_id).first()
    if not user_id:
        result = {
            "code": 204,
            "msg": "请先登录"
        }
        return jsonify(result)
    if not door_id:
        result = {
            "code": 204,
            "msg": "缺少产品id"
        }
        return jsonify(result)
    # if u and d:
    #     if u.number==1:
    #         de = ShoppingCart.query.filter_by(user_id=user_id).first()
    #         db.session.delete(de)
    #         db.session.commit()
    #         return jsonify({"code": 200, "msg": "删除成功"})
    #     if u.number>1:
    #         u.number -=1
    #         return jsonify({"code":200, "msg":"操作成功"})

    de = ShoppingCart.query.filter_by(user_id=user_id, door_id=door_id).first()
    db.session.delete(de)
    db.session.commit()
    return jsonify({"code": 200, "msg": "删除成功"})


# 查看个人用户下的购物车
@shopping.route("/all_shopping_cart/", methods=["POST"])
def all_shopping_cart():
    user_id = request.json["user_id"]
    shoppingcarts = ShoppingCart.query.filter_by(user_id=user_id).all()
    print(shoppingcarts)
    if not shoppingcarts:
        return jsonify({"code": 204, "msg": "空空如也", "data":[]})

    data = []

    for shoppingcart in shoppingcarts:
        d = dict(
            door_id= shoppingcart.door_id,
            number = shoppingcart.number
        )
        data.append(d)

    return jsonify({"code":200, "msg":'id为{}的用户购物车的所有商品的id返回成功'.format(user_id),
                    "data":data})