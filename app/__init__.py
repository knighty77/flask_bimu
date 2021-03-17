from flask import Flask
from config import config, Config
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from redis import StrictRedis

app = Flask(__name__)
db = SQLAlchemy()

redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    Session(app)

    # 注册前台蓝图
    from app.home import home_blue
    app.register_blueprint(home_blue)

    from app.admin import admin_blue
    app.register_blueprint(admin_blue)

    # 后台项目类型蓝图
    from app.admin.type import type_blue
    app.register_blueprint(type_blue)

    return app
