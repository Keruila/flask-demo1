import datetime

from app.extensions import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    is_manager = db.Column(db.Boolean, default=False)
    avatar_url = db.Column(db.Text, nullable=True)  # 图片地址


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_type = db.Column(db.String(30))
    product_name = db.Column(db.String(30))
    image_url = db.Column(db.Text)


class Collect(db.Model):
    __tablename__ = 'collect'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))


class Article(db.Model):
    __tableaname__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publish_time = db.Column(db.DateTime, default=datetime.datetime.now)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text, nullable=False)
    comment = db.relationship('Comment', backref='article')


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_time = db.Column(db.DateTime, default=datetime.datetime.now)
    content = db.Column(db.Text, nullable=False)
