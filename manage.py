from flask import session
from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate

from app import creat_app, db

app = creat_app('development')
manage = Manager(app)

Migrate(app, db)
manage.add_command('db', MigrateCommand)


@app.route('/')
def index():
    session['name'] = 'clwy'
    return session['name']

if __name__ == '__main__':
    app.run()