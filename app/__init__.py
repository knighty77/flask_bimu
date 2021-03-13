from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()

def creat_app(config_name):
    app.config.from_object(config[config_name])
    db.init_app(app)
    return app