# 设置连接数据库的URL
user = 'root'
password = '991124wjr'
database = 'SecondHandCar'


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@localhost/{}'.format(user, password, database)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
