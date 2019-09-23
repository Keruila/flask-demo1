from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

db = SQLAlchemy()
migrate = Migrate(db=db)


# 初始化对象
def config_extensions(app):
    db.init_app(app)
    migrate.init_app(app=app)
