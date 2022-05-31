class Config:
    SECRET_KEY = 'ReposteriaMargalin1'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'proyectosis'

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}