from ..models.user import Door
from flask import Blueprint, jsonify

product = Blueprint("product", __name__, url_prefix="/product")


@product.route('/all/', methods=["GET"])
def get_all_doors():
    """返回所有的门的信息"""
    all_doors = Door.query.all()
    if all_doors:
        data = []
        for door in all_doors:
            door_info = dict(
                id=door.id,
                name=door.name,
                material=door.name,
                category=door.category,
                color=door.color,
                door_type=door.door_type,
                price=door.price,
                opening_closing_mode=door.opening_closing_mode,
                description=door.description,
                img_url=door.img_url,
            )
            data.append({door.id: door_info})
        result = {
            "code": 200,
            'msg': "success",
            'data': data
        }
        return jsonify(result)
    else:
        result = {
            "code": 204,
            'msg': "no data",
            'data': []
        }
        return jsonify(result)


@product.route('/single/<int:door_id>', methods=["GET"])
def get_door_details(door_id):
    """返回一个门的信息"""
    door = Door.query.filter_by(id=door_id).first()
    if door:
        data = dict(
            name=door.name,
            material=door.name,
            category=door.category,
            color=door.color,
            door_type=door.door_type,
            price=door.price,
            opening_closing_mode=door.opening_closing_mode,
            description=door.description,
            img_url=door.img_url,
        )
        result = {
            "code": 200,
            'msg': "success",
            'data': data
        }
        return jsonify(result)
    else:
        result = {
            "code": 204,
            'msg': "no data",
            'data': {}
        }
        return jsonify(result)
