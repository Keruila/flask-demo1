import os
base_dir = os.path.dirname(__file__)
print(base_dir)
class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

#开发环境
class DevelopConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(base_dir, "inter-dev.sqlite")

#测试环境
class TestConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(base_dir, "inter-test.sqlite")
#生产环境的配置
class ProductConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(base_dir, "inter.sqlite")


config = {
    "develop":DevelopConfig,
    "testing":TestConfig,
    "product":ProductConfig,
    "default":DevelopConfig
}
