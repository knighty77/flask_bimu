from flask import Flask
from flask_script import Manager
from config import config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import MigrateCommand, Migrate

app = Flask(__name__)
manage = Manager(app)
db = SQLAlchemy(app)

Migrate(db, app)
manage.add_command('db', MigrateCommand)

app.config.from_object(config['development'])

@app.route('/')
def index():
    return 'Hello Clwy!'

if __name__ == '__main__':
    manage.run()