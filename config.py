class Config:
    DEBUG = None


# 定义开发模式的配置
class developmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/bimu'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

# 定义生产模式的配置
class productionConfig(Config):
    DEBUG = False


# 定义字典，方便取值
config = {
    'development': developmentConfig,
    'production': productionConfig
}
