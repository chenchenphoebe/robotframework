# -*- coding: utf-8 -*-
from flask_migrate import Manager
from flask_migrate import Migrate, MigrateCommand
from zlktqa import app
from exts import db
# 需要映射到数据库中的模型引入进来
from models import User, Question, Answer

manager = Manager(app)

# 使用migrate绑定app和db
migrate = Migrate(app, db)

# 添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)


# if __name__ == "__main__":
#     manager.run()


# 初始化当前项目的迁移的环境
# python manage.py db init

# 做一个迁移文件(versions)
# python manage.py db migrate

# 运行迁移文件(**.py)将表映射到数据库中
# python manage.py db upgrade

#
