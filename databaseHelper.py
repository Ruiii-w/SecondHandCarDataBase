import time

from database import DataBase, UserType, UserTypeAttr, UserAttr, PurchaserAttr, SellerAttr, AgencyAttr, HouseAttr, \
    HouseTypeAttr, HouseStatusAttr, AreaAttr, CollectionAttr, OrderAttr
import time
import datetime
from sqlalchemy import or_, and_


def userTypeMapping(userType):
    if userType == "purchaser":
        userType = 0
    elif userType == 'seller':
        userType = 1
    else:
        userType = 2
    return userType


def houseTypeMapping(houseType):
    if houseType == "normal":
        houseType = 0
    elif houseType == "loft":
        houseType = 1
    else:
        houseType = 2
    return houseType


def areaMapping(area):
    if area == "shenzhen":
        area = 0
    elif area == "college_town":
        area = 1
    else:
        area = 2
    return area


def houseStatusMapping(houseStatus):
    if houseStatus == 'free':
        houseStatus = 0
    elif houseStatus == 'purchased':
        houseStatus = 1
    else:
        houseStatus = 2
    return houseStatus


class DataBaseHelper:
    def __init__(self, db):
        self.db = db
        # self.conn = conn
        # self.cursor = self.conn.cursor()

        '''****************数据库静态资源初始化 start****************'''
        # self.db.drop_all()
        # self.db.create_all()
        # # 用户类别
        # self.userType_insert('0', "purchaser")
        # self.userType_insert('1', "seller")
        # self.userType_insert('2', "agency", orderTimes=999)
        #
        # # 地区
        # self.area_insert("0", "深圳", "深圳赚钱深圳花，一分别想带回家")
        # self.area_insert("1", "深圳大学城", "西丽边边")
        # self.area_insert("2", "哈尔滨工业大学深圳", "四食堂盖3年,深圳速度")
        #
        # # 房屋状态
        # self.houseStatus_insert("0", "闲置", "已被预定,但未出售")
        # self.houseStatus_insert("1", "出售", "已出售")
        # self.houseStatus_insert("2", "预订", "已被预订,但未出售")
        #
        # # 房屋类型
        # self.houseType_insert('0', '平房', "5平米,有个坑")
        # self.houseType_insert('1', '复式', "共3层,每层一个坑")
        # self.houseType_insert('2', '别墅', '全都是坑')

        '''****************数据库静态资源初始化 end****************'''

    def userType_insert(self, typeid, typeName, orderTimes=5):
        userType = UserTypeAttr(user_type_name=typeName, type_id=typeid, limits=orderTimes)
        self.db.session.add(userType)
        self.db.session.commit()
        print("[OK]: {userType} initial successfully!!")

    def user_insert(self, userType, account=None, password=None, register_data=datetime.date.today()):
        if account is None or password is None:
            print("[Error]: {user} insert error!!!")
            return
        register_data_str = register_data.strftime("%Y-%m-%d")
        # print(register_data_str)
        # self.cursor.execute("insert into {}({}, {}, {}, {}) values (%s, %s, %s, %s)".format(
        #     DataBase.user.__tableName__, DataBase.user.account, DataBase.user.userType,
        #     DataBase.user.password, DataBase.user.regist_data),
        #     (account, userType, password, register_data_str))
        user = UserAttr(acc_name=account, pwd=password, register_date=register_data_str, type_id=userType)
        self.db.session.add(user)
        self.db.session.flush()
        userid = user.userid
        # print(userid)
        self.db.session.commit()
        print("[OK]: {user} insert successfully!!!")
        return userid

    def purchaser_insert(self, name, sex, phone, nickname, userid):
        if name is None:
            print("[Error]: {purchaser} insert error!!!")
            return
        purchaser = PurchaserAttr(purchaser_name=name, sex=sex, phone=phone, nickname=nickname, userid=userid)
        self.db.session.add(purchaser)
        self.db.session.commit()
        print("[OK]: {purchaser} insert successfully!!!")

    def seller_insert(self, name, sex, phone, nickname, userid):
        if name is None:
            print("[Error]: {seller} insert error!!!")
            return

        seller = SellerAttr(seller_name=name, sex=sex, phone=phone, nickname=nickname, userid=userid)

        self.db.session.add(seller)
        self.db.session.commit()
        print("[OK]: {seller} insert successfully!!!")

    def agency_insert(self, name, phone, userid):
        if name is None:
            print("[Error]: {agency} insert error!!!")
            return

        agency = AgencyAttr(agency_name=name, phone=phone, userid=userid)

        self.db.session.add(agency)
        self.db.session.commit()
        print("[OK]: {agency} insert successfully!!!")

    def house_insert(self, type_id, status_id, area_id, price, dsp):
        house = HouseAttr(type_id=type_id, status_id=status_id, area_id=area_id, price=price, dsp=dsp)
        self.db.session.add(house)
        self.db.session.commit()
        print("[OK]: {house} insert successfully!!!")

    def houseType_insert(self, type_id, type_name, dsp):
        houseType = HouseTypeAttr(type_id=type_id, type_name=type_name, dsp=dsp)
        self.db.session.add(houseType)
        self.db.session.commit()

    def houseStatus_insert(self, status_id, status_name, dsp):
        houseStatus = HouseStatusAttr(status_id=status_id, status_name=status_name, dsp=dsp)
        self.db.session.add(houseStatus)
        self.db.session.commit()

    def area_insert(self, area_id, area_name, dsp):
        area = AreaAttr(area_id=area_id, area_name=area_name, dsp=dsp)
        self.db.session.add(area)
        self.db.session.commit()

    def order_insert(self, userid, house_id, otime=datetime.date.today()):
        oid = int(userid) * 11 + int(house_id) * 17
        order = OrderAttr(userid=userid, house_id=house_id, oid=oid, otime=otime)
        self.db.session.add(order)
        self.db.session.commit()

    def collection_insert(self, userid, house_id, ctime=datetime.date.today()):
        cid = int(userid) * 11 + int(house_id) * 17
        collection = CollectionAttr(userid=userid, house_id=house_id, cid=cid, ctime=ctime)
        self.db.session.add(collection)
        self.db.session.commit()

    def user_query(self, account=None, userType=None, userid=None, registerData=None):
        if userid is not None:
            return UserAttr.query.get(userid)
        elif account is not None:
            return UserAttr.query.filter_by(acc_name=account).all()
        elif userType is not None:
            return UserAttr.query.filter_by(type_id=userType).all()

    def house_query(self, house_id=None, houseType=None, area=None, price=None):
        if house_id is not None:
            return HouseAttr.query.filter_by(house_id=house_id)

        filter = {
            and_(
                HouseAttr.area_id == area,
                HouseAttr.price <= price,
                HouseAttr.type_id == houseType,
            )
        }
        return HouseAttr.query.filter(*filter).all()

    def house_type_query(self, houseTypeId):

        return HouseTypeAttr.query.get(houseTypeId)

    def house_status_query(self, status_id):
        status = HouseStatusAttr.query.get(status_id)
        print(status)
        return status

    def house_area_query(self, area_id):
        area = AreaAttr.query.get(area_id)
        print(area)
        return area

    def house_query_all(self):
        return HouseAttr.query.all()

    def order_query_all(self, userid):
        orders = OrderAttr.query.filter_by(userid=userid).all()
        print(orders)
        return orders

    def collection_query_all(self, userid):
        return CollectionAttr.query.filter_by(userid=userid).all()

    def user_query_all(self):
        return UserAttr.query.all()

    def house_update(self, house_id, house_status):

        house = HouseAttr.query.filter_by(house_id=house_id).first()

        house.status_id = house_status

        self.db.session.commit()

    def order_delete(self, oid):
        OrderAttr.query.filter_by(oid=oid).delete()

        self.db.session.commit()

    def collection_delete(self, cid):
        CollectionAttr.query.filter_by(cid=cid).delete()

        self.db.session.commit()
