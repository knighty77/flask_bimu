from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate

from app import creat_app, db

app = creat_app('production')
manage = Manager(app)

Migrate(app, db)
manage.add_command('db', MigrateCommand)


@app.route('/')
def index():
    return 'Hello Clwy!'

if __name__ == '__main__':
    app.run()