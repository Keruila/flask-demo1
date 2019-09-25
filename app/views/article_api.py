from ..models.user import Article
from flask import Blueprint, jsonify
from app.extensions import db

article = Blueprint("article", __name__, url_prefix="/article")


@article.route('/add_article/', methods=["POST", "GET"])
def add_article():
    """新增一篇文章"""


@article.route('/delete_article/<int:article_id>', methods=["GET"])
def delete_article(article_id):
    """删除id为article_id的文章"""
    pass


@article.route('/add_comment/<int:article_id>', methods=["POST"])
def add_comment(article_id):
    """在id为article_id的文章下添加一条评论"""


@article.route('/delete_comment/<int:comment_id>', methods=["GET"])
def delete_comment(comment_id):
    """删除id为comment_id的评论"""
    pass


@article.route('/all_comments/<int:article_id>', methods=["POST"])
def get_all_comments(article_id):
    """获得id为article_id的文章下的所有评论"""
    pass


