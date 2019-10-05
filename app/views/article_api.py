from ..models.user import Article, Comment, User
from ..extensions import db
from flask import Blueprint, jsonify, session, request
import os

news = Blueprint("news", __name__, url_prefix="/news")


@news.route('/all_articles/', methods=["POST"])
def get_all_article():
    """获得所有文章"""
    # user_id = request.json["id"]
    # user = User.query.filter_by(id=user_id).first()
    # article = Article.query.filter_by(user_id=user_id)
    all_article = Article.query.all()


@news.route('/article/', methods=["POST"])
def get_article_by_id():
    """根据文章id返回文章所有信息"""
    try:
        article_id = request.json["id"]
        article = Article.query.filter_by(id=article_id).first()
        content = article.content.split("*")  # list
        # user = article.user_id.username
        username = User.query.get(article.user_id).username
        img_dir = "./app/static/img/article/" + article.img_url
        imgs = os.listdir(img_dir)
        img_list = []
        for img in imgs:
            img_path = os.path.join('/static/img/article/', article.img_url, img)
            img_list.append(img_path)
        data = dict(
            id=article.id,
            publish_time=article.publish_time,
            title=article.title,
            content=content,
            user_id=username,
            img_list=img_list
        )
        result = {
            'code': 200,
            'msg': '请求成功',
            'data': data
        }
    except Exception as e:
        print(e)
        result = {
            'code': 204,
            'msg': '出错',
            'data': {}
        }
    return jsonify(result)

