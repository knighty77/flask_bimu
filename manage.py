from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
from app import create_app, db, models

app = create_app('development')
manage = Manager(app)
Migrate(app, db)
manage.add_command('db', MigrateCommand)

if __name__ == '__main__':
    print(app.url_map)  # 输出路由映射
    manage.run()
