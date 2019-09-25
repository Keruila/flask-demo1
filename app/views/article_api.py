from ..models.user import Article,Comment
from flask import Blueprint, jsonify, request, session
from ..extensions import db
from flask import Blueprint, jsonify, session, request

article = Blueprint("article", __name__, url_prefix="/article")

# 增加文章
@article.route('/add_article/', methods=["POST"])
def add_article():
    """新增一篇文章"""
    content = request.form["content"]
    title = request.form["title"]
    user_id = session.get("user_id", "null")
    if user_id != "null":
        save = Article(content=content, title=title, user_id=user_id)
        db.session.add(save)
        db.session.commit()
        return jsonify({"code": 200, "user_id": user_id, "msg": "发表成功"})
    else:
        return jsonify({"code": 201, "msg": "请先登录"})

# 删除文章
@article.route('/delete_article/<int:article_id>/', methods=["POST"])
def delete_article(article_id):
    """删除id为article_id的文章"""
    save = Article.query.get(article_id)
    if save:
        db.session.delete(save)
        db.session.commit()
        return jsonify({"code": 200, "msg": "删除成功"})
    return jsonify({"code": 201, "msg": "您还没有发表过文章"})


@article.route('/add_comment/<int:article_id>', methods=["POST"])
def add_comment(article_id):
    """在id为article_id的文章下添加一条评论"""
    content = request.form["content"]
    user_id = session.get("user_id")
    if user_id:
        save = Comment(content=content, user_id=user_id, article_id=article_id)
        db.session.add(save)
        db.session.commit()
        return jsonify({"code": 200, "msg": "评论成功"})
    else:
        return jsonify({"code": 201, "msg": "请先登录后再来评论"})

# 删除id为comment_id的评论
@article.route('/delete_comment/<int:comment_id>/', methods=["POST"])
def delete_comment(comment_id):
    """删除id为comment_id的评论"""
    save = Comment.query.get(comment_id)
    if save is None:
        return jsonify({"code": 201, "msg": "未找到该评论"})
    else:
        db.session.delete(save)
        db.session.commit()
        return jsonify({"code": 200, "msg": "删除成功"})


# 获得id为article_id的文章下的所有评论
def replace_id_url(tasks):
    return dict(content=tasks.content, comment_time=tasks.comment_time)


@article.route('/all_comments/<int:article_id>/', methods=["POST"])
def get_all_comments(article_id):
    save = Comment.query.filter_by(article_id=article_id).all()
    if len(save) == 0:
        return jsonify({"code": 201, "msg": "没有找到您需要的内容"})
    else:
        return jsonify({"code": 200, "msg": "获取成功", "data": list(map(replace_id_url, save))})


