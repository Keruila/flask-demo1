# 启动控制文件
from app import create_app

from flask_script import Manager
from flask_migrate import MigrateCommand
from flask_cors import CORS

app = create_app("default")
CORS(app, supports_credentials=True)
manager = Manager(app)

manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()


# commit test
# sdfsdfas
