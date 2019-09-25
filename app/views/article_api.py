from ..models.user import Article, Comment
from flask import Blueprint, jsonify, request, session
from ..extensions import db

article = Blueprint("article", __name__, url_prefix="/article")


@article.route('/add_article/', methods=["POST"])
def add_article():
    """新增一篇文章"""
    content = request.form["content"]
    title = request.form["title"]
    user_id = session.get("user_id", "null")
    if user_id != "null":
        sav = Article(content=content, title=title, user_id=user_id)
        db.session.add(sav)
        db.session.commit()
        return jsonify({"code": 200, "user_id": user_id, "msg": "发表成功"})
    else:
        return jsonify({"code": 201, "msg": "请先登录"})


@article.route('/delete_article/<int:article_id>/', methods=["POST"])
def delete_article(article_id):
    """删除id为article_id的文章"""
    u = Article.query.get(article_id)
    if u:
        db.session.delete(u)
        db.session.commit()
        return jsonify({"code": 200, "msg": "删除成功"})
    return jsonify({"code": 201, "msg": "您还没有发表过文章"})


@article.route('/add_comment/<int:article_id>/', methods=["POST"])
def add_comment(article_id):
    """在id为article_id的文章下添加一条评论"""
    pass


@article.route('/delete_comment/<int:comment_id>/', methods=["POST"])
def delete_comment(comment_id):
    """删除id为comment_id的评论"""
    pass


@article.route('/all_comments/<int:article_id>/', methods=["POST"])
def get_all_comments(article_id):
    """获得id为article_id的文章下的所有评论"""
    pass
