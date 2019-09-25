import os
import redis

base_dir = os.path.dirname(__file__)
print(base_dir)


class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # redis配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # session配置
    SECRET_KEY = "iHome"
    # 将session存储到redis中
    SESSION_TYPE = "redis"
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 14  # 秒


# 开发环境
class DevelopConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(base_dir, "inter-dev.sqlite")


# 测试环境
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(base_dir, "inter-test.sqlite")


# 生产环境的配置
class ProductConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(base_dir, "inter.sqlite")


config = {
    "develop": DevelopConfig,
    "testing": TestConfig,
    "product": ProductConfig,
    "default": DevelopConfig
}
