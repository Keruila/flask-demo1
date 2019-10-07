from ..models.user import Order, ShoppingCart, SubOrder
from ..extensions import db
from flask import Blueprint, jsonify, request
import os
from alipay import AliPay
from datetime import datetime

alipay = Blueprint("alipay", __name__)


@alipay.route("/orders/payment/", methods=["POST"])
def order_pay():
    user_id = request.json["user_id"]
    order_id = request.json['order_id']
    total_price = request.json['total_price']
    print("用户id", user_id, "order", order_id, total_price)
    order = Order.query.filter_by(id=order_id, user_id=user_id, status=0).first()
    if order is None:
        return jsonify({"code": 201, "msg": "订单信息有误"})
    else:
        # 实例化支付应用
        alipay = AliPay(
            appid="2016101200669783",
            app_notify_url=None,
            app_private_key_path=os.path.join(os.path.dirname(__file__), "keys/alipay_private_key.pem"),
            alipay_public_key_path=os.path.join(os.path.dirname(__file__), "keys/alipay_public_key.pem"),
            sign_type="RSA2"
        )

        # 发起支付请求
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,  # 订单号，多次请求不能一样
            total_amount=total_price,  # 支付金额
            subject="双杰木门",  # 交易主题
            return_url="http://localhost:8080/#/pay_success/",
            notify_url=None
        )

        pay_url = "https://openapi.alipaydev.com/gateway.do?" + order_string
        return jsonify({"code": 200, "msg": pay_url})


@alipay.route('/pay_success/', methods=['POST'])
def check_pay():
    order_id = request.json["order_id"]
    if not order_id:
        result = {
            'code': 204,
            'msg': '缺少订单id'
        }
        return jsonify(result)
    _order = Order.query.filter_by(id=order_id).first()
    o = SubOrder.query.filter_by(order_id=order_id).first()
    print(o)
    if not _order:
        result = {
            'code': 204,
            'msg': '没有此订单'
        }
        return jsonify(result)
    user_id = _order.user_id
    door_id = o.door_id
    de = ShoppingCart.query.filter_by(user_id=user_id, door_id=door_id).first()
    db.session.delete(de)
    if not de:
        return jsonify({"code": 200, "msg": "信息错误"})
    _order.status = 1  # 变为已付款
    _order.pay_time = datetime.now()
    db.session.commit()
    result = {
        'code': 200,
        'msg': '状态改为已付款'
    }
    return jsonify(result)
