import time

from flask import Blueprint, request, jsonify

from app.extensions import db
from ..models.user import Order, SubOrder
import random


order = Blueprint("order", __name__, url_prefix='/order')


@order.route('/add/', methods=["POST"])
def add_order():
    user_id = request.json['user_id']
    total_price = request.json['total_price']
    doors = request.json['doors']  # 门id和其数量组成的list，如： [{"id": 1, "count": 2}, {"id": 2, "count": 3}]

    error = None
    if not user_id:
        error = "缺少user_id"
    if not total_price:
        error = "缺少总价"
    if not doors:
        error = "缺少门列表"
    if error:
        result = {
            "code": 204,
            "msg": error
        }
        return jsonify(result)

    random_num = "".join([str(random.randint(0, 9)) for i in range(5)])
    order_id = str(user_id) + random_num + str(int(time.time()))  # 生成随机唯一订单号

    new_order = Order(
        id=order_id,
        user_id=user_id,
        status=0,
        total_price=total_price,
        address="翻斗小区"
    )
    db.session.add(new_order)

    for door in doors:
        sub_order = SubOrder(
            order_id=order_id,
            door_id=door["id"],
            count=door["count"]
        )
        db.session.add(sub_order)
    db.session.commit()
    result = {
        'code': 200,
        'msg': '订单已生成'
    }
    return jsonify(result)
