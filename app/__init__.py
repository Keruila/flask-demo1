# 写实例化app的代码
# 工厂函数
from flask import Flask
from app.config import config
from app.views.user import auth
from app.views.article_api import news
from app.views.index_api import index
from app.views.door_api import product
from app.views.shopping_api import shopping
from app.views.order_api import order
from app.views.search import search
from app.views.orders_api import alipay
from app.views.auth_code_api import check_code
from app.extensions import config_extensions
from app.admin_view import init_admin
from app.models.user import User
from flask_cors import CORS




def create_app(config_name):
    # 创建app实例
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    # "develop": DevelopConfig,
    # "testing": TestConfig,
    # "product": ProductConfig,
    # "default": DevelopConfig
    if config_name not in config:
        config_name = "default"
    # 把config文件中的类进行实例化
    # https://blog.csdn.net/weixin_42102783/article/details/80146861
    # flask下面from_object这个函数什么意思
    # 就是对config配置文件中的类进行实例化的操作

    app.config.from_object(config[config_name])

    app.register_blueprint(auth)
    app.register_blueprint(index)
    app.register_blueprint(product)
    app.register_blueprint(news)
    app.register_blueprint(shopping)
    app.register_blueprint(alipay)
    app.register_blueprint(search)
    app.register_blueprint(order)
    app.register_blueprint(check_code)
    config_extensions(app)
    init_admin(app)
    return app
