from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask import Flask, render_template
from flask import request
import mysql.connector

class MySQLAlchemy(SQLAlchemy):
    Column: callable
    String: callable
    Integer: callable
    Date: callable
    ForeignKey: callable
    Boolean: callable
    relationship: callable
    Float: callable
    Text: callable


class UserView:
    # __tableName__ = "用户"
    # account = "账号"
    # userid = "id"
    # userType = "用户类别编号"
    # password = "密码"
    # regist_data = "注册日期"
    def __init__(self, user):
        self.acc_name = user.acc_name
        self.userid = user.userid
        self.pwd = user.pwd
        self.register_date = user.register_date
        self.type_id = user.type_id


class UserType:
    __tableName__ = "用户类别"
    name = "用户类别名称"
    id = "用户类别编号"
    appointmentLimit = "预约次数"


class Seller:
    __tableName__ = "卖家"
    name = "姓名"
    sex = "性别"
    phone = "联系电话"
    nickname = "昵称"
    id = "卖家编号"
    userid = 'id'


class Purchaser:
    __tableName__ = "买家"
    name = "姓名"
    sex = "性别"
    phone = "联系电话"
    nickname = "昵称"
    id = "买家编号"
    userid = 'id'


class Agency:
    __tableName__ = "中介"
    id = "中介编号"
    phone = "联系电话"
    name = "中介名称"
    userid = 'id'


class House:
    __tableName__ = "二手房"

    id = '二手房编号'
    houseType = "房型编号"
    houseStatus = "状态编号"
    area = "地区编号"
    price = "二手房价格"
    description = "描述"


class HouseType:
    __tableName__ = "二手房类别"
    id = "房型编号"
    name = "房型名称"
    description = "房型描述"


class HouseStatus:
    __tableName__ = "二手房状态"
    id = "状态编号"
    name = "状态名称"
    description = "状态描述"


class Area:
    __tableName__ = "地区"
    id = "地区编号"
    name = "地区名称"
    description = "地区描述"


class Order:
    __tableName__ = "订单"

    userid = 'id'
    houseId = "二手房编号"
    time = "预约时间"


class Collection:
    __tableName__ = "收藏"

    userid = 'id'
    houseId = "二手房编号"
    time = "收藏时间"


class DataBase:
    name = "SecondHandCar"
    app = Flask(__name__)  # 引入Flask
    app.config.from_object(Config)

    db = SQLAlchemy(app)
    # userType = UserType()
    # seller = Seller()
    # purchaser = Purchaser()
    # agency = Agency()
    # house = House()
    # houseType = HouseType()
    # houseStatus = HouseStatus()
    # area = Area()
    # order = Order()
    # collection = Collection()


'''***************SQLAlchemy Attributes***************'''


class UserAttr(DataBase.db.Model):
    __tableName__ = "user_attr"

    acc_name = DataBase.db.Column(DataBase.db.String(32))
    userid = DataBase.db.Column(DataBase.db.Integer, primary_key=True, autoincrement=True)

    pwd = DataBase.db.Column(DataBase.db.String(32))
    register_date = DataBase.db.Column(DataBase.db.Date)

    type_id = DataBase.db.Column(DataBase.db.Integer, DataBase.db.ForeignKey("user_type_attr.type_id"))
    # def __init__(self, account, userType, password, register_date):
    #     self.account = account
    #     self.userType = userType
    #     self.password = password
    #     self.regist_date = register_date


class UserTypeAttr(DataBase.db.Model):
    __tableName__ = "user_type_attr"
    user_type_name = DataBase.db.Column(DataBase.db.String(10))
    type_id = DataBase.db.Column(DataBase.db.Integer, primary_key=True)
    limits = DataBase.db.Column(DataBase.db.Integer)

    # users = DataBase.db.relationship("UserAttr", backref="usertype")

    # def __init__(self, name, id, appointmentLimit):
    #     self.name = name
    #     self.id = id
    #     self.appointmentLimit = appointmentLimit


class SellerAttr(DataBase.db.Model):
    __tableName__ = "seller_attr"
    seller_name = DataBase.db.Column(DataBase.db.String(32))
    sex = DataBase.db.Column(DataBase.db.Boolean)
    phone = DataBase.db.Column(DataBase.db.String(15))
    nickname = DataBase.db.Column(DataBase.db.String(20))
    id = DataBase.db.Column(DataBase.db.Integer, primary_key=True, autoincrement=True)
    userid = DataBase.db.Column(DataBase.db.Integer, DataBase.db.ForeignKey("user_attr.userid"))


class PurchaserAttr(DataBase.db.Model):
    __tableName__ = "purchaser_attr"
    purchaser_name = DataBase.db.Column(DataBase.db.String(32))
    sex = DataBase.db.Column(DataBase.db.Boolean)
    phone = DataBase.db.Column(DataBase.db.String(15))
    nickname = DataBase.db.Column(DataBase.db.String(20))
    id = DataBase.db.Column(DataBase.db.Integer, primary_key=True, autoincrement=True)
    userid = DataBase.db.Column(DataBase.db.Integer, DataBase.db.ForeignKey("user_attr.userid"))


class AgencyAttr(DataBase.db.Model):
    __tableName__ = "agency_attr"
    id = DataBase.db.Column(DataBase.db.Integer, primary_key=True, autoincrement=True)
    phone = DataBase.db.Column(DataBase.db.String(15))
    agency_name = DataBase.db.Column(DataBase.db.String(20))
    userid = DataBase.db.Column(DataBase.db.Integer, DataBase.db.ForeignKey("user_attr.userid"))


class HouseAttr(DataBase.db.Model):
    __tableName__ = "house_attr"

    house_id = DataBase.db.Column(DataBase.db.Integer, primary_key=True, autoincrement=True)
    type_id = DataBase.db.Column(DataBase.db.Integer, DataBase.db.ForeignKey("house_type_attr.type_id"))
    status_id = DataBase.db.Column(DataBase.db.Integer,
                                     DataBase.db.ForeignKey("house_status_attr.status_id"))
    area_id = DataBase.db.Column(DataBase.db.Integer, DataBase.db.ForeignKey("area_attr.area_id"))
    price = DataBase.db.Column(DataBase.db.Float)
    dsp = DataBase.db.Column(DataBase.db.Text)


class HouseTypeAttr(DataBase.db.Model):
    __tableName__ = "house_type_attr"

    type_id = DataBase.db.Column(DataBase.db.Integer, primary_key=True)
    type_name = DataBase.db.Column(DataBase.db.Text)
    dsp = DataBase.db.Column(DataBase.db.Text)

    # houses = DataBase.db.relationship("HouseAttr", backref="housetype")


class HouseStatusAttr(DataBase.db.Model):
    __tableName__ = "house_status_attr"
    status_id = DataBase.db.Column(DataBase.db.Integer, primary_key=True)
    status_name = DataBase.db.Column(DataBase.db.Text)
    dsp = DataBase.db.Column(DataBase.db.Text)

    # houses = DataBase.db.relationship("HouseAttr", backref="housetype")


class AreaAttr(DataBase.db.Model):
    __tableName__ = "area_attr"

    area_id = DataBase.db.Column(DataBase.db.Integer, primary_key=True)
    area_name = DataBase.db.Column(DataBase.db.Text)
    dsp = DataBase.db.Column(DataBase.db.Text)

    # houses = DataBase.db.relationship("HouseAttr", backref="housetype")


class OrderAttr(DataBase.db.Model):
    __tableName__ = "order_attr"

    userid = DataBase.db.Column(DataBase.db.Integer, DataBase.db.ForeignKey("user_attr.userid"), primary_key=True)
    house_id = DataBase.db.Column(DataBase.db.Integer, DataBase.db.ForeignKey("house_attr.house_id"), primary_key=True)
    otime = DataBase.db.Column(DataBase.db.Date)
    oid = DataBase.db.Column(DataBase.db.Integer)

class CollectionAttr(DataBase.db.Model):
    __tableName__ = "collection_attr"

    userid = DataBase.db.Column(DataBase.db.Integer, DataBase.db.ForeignKey("user_attr.userid"), primary_key=True)
    house_id = DataBase.db.Column(DataBase.db.Integer, DataBase.db.ForeignKey("house_attr.house_id"), primary_key=True)
    ctime = DataBase.db.Column(DataBase.db.Date)
    cid = DataBase.db.Column(DataBase.db.Integer)
