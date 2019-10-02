import datetime

from app.extensions import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    is_manager = db.Column(db.Boolean, default=False)
    avatar_url = db.Column(db.Text, nullable=True)  # 图片地址
    article = db.relationship('Article', backref='user')


# class Product(db.Model):
#     __tablename__ = 'product'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     product_type = db.Column(db.String(30), nullable=False)  # 型号
#     product_name = db.Column(db.String(30), nullable=False)
#     image_url = db.Column(db.Text)


class Collect(db.Model):
    __tablename__ = 'collect'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    door_id = db.Column(db.Integer, db.ForeignKey('door.id'), nullable=False)


class ShoppingCart(db.Model):
    __tablename__ = 'shoppingcart'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    door_id = db.Column(db.Integer, db.ForeignKey('door.id'), nullable=False)
    number = db.Column(db.Integer, default=1)


class Article(db.Model):
    __tableaname__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publish_time = db.Column(db.DateTime, default=datetime.datetime.now)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment = db.relationship('Comment', backref='article')
    img_url = db.Column(db.String(50))
    is_delete = db.Column(db.Integer, default=0)  # 0：没删除， 1：已删除


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment_time = db.Column(db.DateTime, default=datetime.datetime.now)
    content = db.Column(db.Text, nullable=False)
    is_delete = db.Column(db.Integer, default=0)  # 0：没删除， 1：已删除


class Door(db.Model):
    __tablename__ = 'door'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, default="双杰木门")
    category = db.Column(db.String(20), nullable=False)
    material = db.Column(db.String(10), nullable=False)  # 材质
    color = db.Column(db.String(10), nullable=False)
    door_type = db.Column(db.String(10), nullable=False)  # 型号
    price = db.Column(db.Integer, nullable=False)
    opening_closing_mode = db.Column(db.String(20))  # 可为空
    description = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(30))  # 暂时设置可为空


class DecoratorCase(db.Model):
    __tablename__ = 'decorator_case'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(30), nullable=False)
    img_dir_url = db.Column(db.String(30))  # 设置为一个文件夹，里面放此家装案例的所有图片
    description = db.Column(db.Text)
