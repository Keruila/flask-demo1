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
        total_price=total_price
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
        'msg': '订单已生成',
        'order_id': order_id
    }
    return jsonify(result)


@order.route('/all/', methods=["POST"])
def all_orders():
    user_id = request.json['user_id']
    if not user_id:
        result = {
            'code': 204,
            'msg': '缺少user_id',
        }
        return jsonify(result)

    orders = Order.query.filter_by(user_id=user_id).all()  # 该用户的所有订单
    data = []
    for o in orders:
        if o.status == 0:
            status = "未付款"
        elif o.status == 1:
            status = "已付款"
        else:
            status = "未付款"

        doors = []
        for g in o.goods:
            good_info = dict(
                id=g.id,
                count=g.count
            )
            doors.append(good_info)

        order_info = dict(
            id=o.id,
            status=status,
            total_price=o.total_price,
            order_generation_time=o.order_generation_time,
            goods=doors
        )
        data.append(order_info)
    result = {
        'code': 200,
        'msg': '成功',
        'data': data
    }
    return jsonify(result)
