#写实例化app的代码
#工厂函数
from flask import Flask
from app.config import config
from app.views.user import user
from app.extensions import config_extensions
from app.models.user import User
def create_app(config_name):
    #创建app实例
    app = Flask(__name__)
    # "develop": DevelopConfig,
    # "testing": TestConfig,
    # "product": ProductConfig,
    # "default": DevelopConfig
    if config_name not in config:
        config_name = "default"
    #把config文件中的类进行实例化
#https://blog.csdn.net/weixin_42102783/article/details/80146861
    # flask下面from_object这个函数什么意思
    #就是对config配置文件中的类进行实例化的操作

    app.config.from_object(config[config_name])

    app.register_blueprint(user)
    config_extensions(app)
    return app