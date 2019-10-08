#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: Keruila
@time: 2019/09/26
@file: admin-view.py
"""
import os

from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask import url_for, g, flash, request, redirect, render_template
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from .extensions import db
from .models.user import User, Article, Collect, Door, DecoratorCase, Order, ShoppingCart, SubOrder
from flask_login import LoginManager, login_required
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash


class MyModelView(ModelView):
    """进行权限控制"""
    def is_accessible(self):
        return current_user.is_authenticated


# class UserView(ModelView):
class SubOrderView(ModelView):
    column_list = [
        'order_id', 'door_id', 'count'
    ]
    can_create = False
    can_edit = False
    can_delete = False


class CollectView(ModelView):
    # can_create = False
    can_edit = False
    # can_delete = False


class OrderView(ModelView):
    column_list = [
        'user', 'status', 'total_price', 'order_generation_time',
        'pay_time', 'goods'
    ]
    can_create = False
    can_edit = False
    can_delete = False


class ShoppingCartView(ModelView):
    can_create = False
    can_edit = False
    can_delete = False



class ImgManage(FileAdmin):
    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(BaseView):
    @expose('/')
    @login_required
    def logout(self):
        logout_user()
        flash('Good Bye')
        return self.render('admin/index.html')

    def is_accessible(self):
        return current_user.is_authenticated

    # def inaccessible_callback(self, name, **kwargs):
    #     return url_for('admin')


class LoginView(BaseView):
    @expose("/", methods=["GET", "POST"])
    def login(self):
        if current_user.is_authenticated:
            return self.render('admin/re_login.html')
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            if not username or not password:
                flash('缺少用户名或密码')
                return redirect(url_for('login'))
            user = User.query.filter_by(username=username).first()
            if not user.is_manager:
                flash('你不是管理员')
                return redirect(url_for('login'))

            if username == user.username and check_password_hash(user.password, password):
                login_user(user)
                flash('登录成功')
                return redirect(url_for('admin.index'))

            flash('密码或用户名错误')
            return redirect(url_for('login'))
        return self.render('admin/admin_login.html')


def init_admin(app):
    admin = Admin(app, name="后台管理系统", template_mode='bootstrap3')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Article, db.session))
    admin.add_view(MyModelView(DecoratorCase, db.session))
    admin.add_view(CollectView(Collect, db.session))
    admin.add_view(MyModelView(Door, db.session))
    admin.add_view(ShoppingCartView(ShoppingCart, db.session))
    admin.add_view(OrderView(Order, db.session, endpoint='the_order'))
    admin.add_view(SubOrderView(SubOrder, db.session))
    # 文件管理
    admin.add_view(ImgManage('app/static/img/'))
    admin.add_view(LogoutView(name='登出'))
    admin.add_view(LoginView(name='登录', endpoint='admin_login'))

    login_manager = LoginManager(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
