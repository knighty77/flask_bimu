from redis import StrictRedis

class Config:
    DEBUG = None
    SECRET_KEY = 'clwy'

    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/bimu'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    REDIS_HOST = '127.0.0.1'  # 配置 Redis 主机地址
    REDIS_PORT = 6379  # 配置 Redis 本地端口
    SESSION_TYPE = 'redis'  # 连接类型
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 实例化传入参数
    SESSION_USE_SIGNER = True  # 签名
    PERMANENT_SESSION_LIFETIME = 86400

# 定义开发模式的配置
class developmentConfig(Config):
    DEBUG = True

# 定义生产模式的配置
class productionConfig(Config):
    DEBUG = False

# 定义字典，方便取值
config = {
    'development': developmentConfig,
    'production': productionConfig
}
