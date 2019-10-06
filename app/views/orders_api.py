from ..models.user import Order
from ..extensions import db
from flask import Blueprint, jsonify, request
import os
from alipay import AliPay

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
    order = Order.query.filter_by(id=order_id).first()
    order.status = 1
    db.session.commit()
    return jsonify({'code': 200})
