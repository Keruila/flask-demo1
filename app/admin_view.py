#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: Keruila
@time: 2019/09/26
@file: admin-view.py
"""
import os

from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from .extensions import db
from .models.user import User, Article, Comment, Door


class MyModelView(ModelView):
    # @expose('/')
    # def index(self):
    #     return self.render('index.html')
    """进行权限控制"""
    pass


def init_admin(app):
    admin = Admin(app, name="后台管理系统")
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Article, db.session))
    admin.add_view(MyModelView(Comment, db.session))
    admin.add_view(MyModelView(Door, db.session))
    # 文件管理
    admin.add_view(FileAdmin('app/static/img/', "文件管理"))

