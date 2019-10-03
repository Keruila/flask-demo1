from app.models.user import Door
from flask import request
import re
from flask import Blueprint, jsonify, abort
# from aip import AipNlp
search= Blueprint("search", __name__,url_prefix="/s")
def replace_id_url(tasks):
    return dict(
        id=tasks.id,
        name=tasks.name,
        category=tasks.category,
        material=tasks.material,
        color=tasks.color,
        door_type=tasks.door_type,
        price=tasks.price,
        opening_closing_mode=tasks.opening_closing_mode,
        description=tasks.description,
        img_url= tasks.img_url
  )


@search.route("/arch/", methods=["POST"])
def search_keywords():

    keyword = request.json["keyword"]
    s ={"木门","欧式","古典","美式","现代","法式","地中海",
      "原木","玻璃","平开门式","推拉门式"}
    n1 =re.search("木门", keyword)
    c1 =re.search("欧式|古典|美式|现代|法式|地中海", keyword)
    c2 =re.search("原木|玻璃|木", keyword)
    c3 =re.search("平开|门式|推拉", keyword)
    c4 =re.search("", keyword)
    c5 =re.search("", keyword)
    if n1:
        names = Door.query.filter_by(name="木门").all()
        return jsonify({"data": list(map(replace_id_url, names))})
    if c1:
        # print(c1[0])
        categorys =  Door.query.filter_by(category=c1[0]).all()
        return jsonify({"data": list(map(replace_id_url, categorys))})
    if c2:
          materials =  Door.query.filter(Door.material.like("%" + c2[0] + "%"))
          return jsonify({"data": list(map(replace_id_url, materials))})
    if c3:
          opening_closing_modes =  Door.query.filter(Door.opening_closing_mode.like("%" + c3[0] + "%"))
          return jsonify({"data": list(map(replace_id_url, opening_closing_modes))})
    return jsonify({"code":"本店铺暂时还没有该商品请等待通知"})
