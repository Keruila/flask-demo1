from flask import Blueprint, request, jsonify
from ..models.user import DecoratorCase
import os

index = Blueprint("index", __name__)


# @index.route("/")
# def index():
#     return "剑阁峥嵘而崔嵬，一夫当关，万夫莫开"


@index.route("/rotation/", methods=["GET"])
def rotation_chart():
    rotation_path = "./app/static/img/rotation/"
    img_list = os.listdir(rotation_path)
    if img_list:
        data = []
        for img in img_list:
            img_path = os.path.join("/static/img/rotation/", img)
            data.append({"img": img_path})
        result = {
            "code": 200,
            "msg": "请求成功",
            "data": data
        }
        return jsonify(result)
    else:
        result = {
            "code": 204,
            "msg": "没有数据可返回",
            "data": []
        }
        return jsonify(result)


@index.route("/case/", methods=["GET"])
def decoration_case():
    decoration_path = "app/static/img/case/index_case"
    img_list = os.listdir(decoration_path)
    if img_list:
        data = []
        for img in img_list:
            img_path = os.path.join("/static/img/case/index_case", img)
            data.append({"img": img_path})
        result = {
            "code": 200,
            "msg": "请求成功",
            "data": data
        }
        return jsonify(result)
    else:
        result = {
            "code": 204,
            "msg": "没有数据可返回",
            "data": []
        }
        return jsonify(result)


@index.route('/all_case/', methods=["GET"])
def decoration_case_on_detail():
    all_case = DecoratorCase.query.all()
    if all_case:
        data = []
        for case in all_case:
            img_list = os.listdir(os.path.join('app/static/img/case', case.img_dir_url))
            img_path = []
            for img in img_list:
                img_path.append(os.path.join('/static/img/case/', case.img_dir_url, img))
            case_info = dict(
                id=case.id,
                address=case.address,
                img_path=img_path,
                description=case.description
                )
            data.append(case_info)
        result = {
            'code': 200,
            'message': '成功',
            'data': data
        }
    else:
        result = {
            'code': 203,
            'message': '没有数据',
            'data': []
        }
    return jsonify(result)


@index.route('/case/<int:case_id>', methods=["GET"])
def get_case_by_id(case_id):
    case = DecoratorCase.query.filter_by(id=case_id).first()
    if not case:
        result = {
            'code': 203,
            'message': '未找到',
            'data': []
        }
        return jsonify(result)
    target_dir = os.path.join('app/static/img/case', case.img_dir_url)
    if not target_dir:  # 没有家装案例的文件夹
        img_path = ['/static/img/case/show_if_no_img.jpg']
    else:
        img_list = os.listdir(target_dir)
        if img_list:  # 有文件夹，其中为空
            img_path = []
            for img in img_list:
                img_path.append(os.path.join('/static/img/case/', case.img_dir_url, img))
        else:
            img_path = ['/static/img/case/show_if_no_img.jpg']

    case_info = dict(
        id=case.id,
        address=case.address,
        img_path=img_path,
        description=case.description
    )

    result = {
        'code': 200,
        'message': '成功',
        'data': [case_info]
    }
    return jsonify(result)


@index.route("/video/", methods=["GET"])
def video():
    result = {
        'code': 200,
        'msg': 'success',
        'img_url': "/static/video/test.mp4"
    }
    return jsonify(result)
