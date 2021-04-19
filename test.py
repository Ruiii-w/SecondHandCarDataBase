from flask import Flask, render_template
from flask import request
import flask_sqlalchemy
import mysql.connector
from databaseHelper import DataBaseHelper, houseTypeMapping, areaMapping, userTypeMapping, houseStatusMapping
from database import DataBase, UserView, UserAttr

# conn = mysql.connector.connect(user="root", password="991124wjr", database=DataBase.name)  # 数据库连接
# cursor = conn.cursor()
#
databaseHelper = DataBaseHelper(DataBase.db)

User = None


class LoginUser:
    def __init__(self, user):
        self.user = user


@DataBase.app.route('/', methods=['GET'])  # 跳转至login.html，请求方式GET
def show():
    return render_template('login.html')


@DataBase.app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']  # 界面传值
        password = request.form['password']  # 界面传值
        if len(username) == 0 | len(password) == 0:
            return render_template('login.html')
        users = databaseHelper.user_query(account=username)
        for user in users:
            if user.pwd == password:
                global User
                User = LoginUser(user)
                user_view = UserView(user)
                user_dict = dict(
                    (name, getattr(user_view, name)) for name in dir(user_view) if not name.startswith('__'))
                # return render_template("homePage.html", user=user_dict)
                if user.type_id == 0:
                    return render_template("buy.html", user=User)
                elif user.type_id == 1:
                    return render_template("sell.html", user=User)
                else:
                    return render_template("agency.html", user=User)


@DataBase.app.route('/regist', methods=['POST', 'GET'])  # 表单提交
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        user = request.form.get('user')
        pw = request.form.get('pw')
        nickname = request.form.get('nickname')
        sex = request.form.get('sex')
        userType = request.form.get('userType')  # 返回select的value值
        # print(userType)
        phone = request.form.get("phone")
        # 把注册信息加入user表

        userType = userTypeMapping(userType)
        if sex == '女':
            sex = 0
        else:
            sex = 1
        userid = databaseHelper.user_insert(account=user, password=pw, userType=userType)

        if userType == 0:
            databaseHelper.purchaser_insert(name=user, sex=sex, phone=phone, nickname=nickname, userid=userid)
        elif userType == 1:
            databaseHelper.seller_insert(name=user, sex=sex, phone=phone, nickname=nickname, userid=userid)
        else:
            databaseHelper.agency_insert(name=user, phone=phone, userid=userid)

        return '<h>注册成功！请登录。</h><form action="/login" method="get"><p><button type="submit">返回登录</button></p></form>'


@DataBase.app.route("/search", methods=['POST', 'GET'])
def search():
    switch = request.form.get("my-house-list")
    if switch == 'houses':
        houses = databaseHelper.house_query_all()
        return render_template('homePage.html', houses=houses)
    switch = request.form.get("my-order-list")
    if switch == 'orders':
        orders = databaseHelper.order_query_all(User.user.userid)
        print(orders)
        return render_template('orders.html', orders=orders)
    switch = request.form.get("my-collection-list")
    if switch == 'collections':
        collections = databaseHelper.collection_query_all(User.user.userid)
        return render_template('collections.html', collections=collections)

    houseType = request.form.get("houseType")
    houseType_id = houseTypeMapping(houseType)
    area = request.form.get("area")
    area_id = areaMapping(area)
    maxPrice = request.form.get("maxPrice")

    houses = databaseHelper.house_query(houseType=houseType_id, area=area_id, price=maxPrice)
    # print(houses)
    # for house in houses:
    #     house.type_id = houseType
    #     house.status_id = databaseHelper.house_status_query(house.status_id).status_name
    #     house.area_id = area
    return render_template('houses.html', houses=houses)


@DataBase.app.route("/sell", methods=["POST"])
def sell():
    switch = request.form.get("my-house-list")
    print(switch)
    if switch == 'houses':
        houses = databaseHelper.house_query_all()
        return render_template('homePage.html', houses=houses)

    houseType = houseTypeMapping(request.form.get("houseType"))
    area = areaMapping(request.form.get("area"))
    price = request.form.get("expectedPrice")
    dsp = request.form.get("description")
    databaseHelper.house_insert(type_id=houseType, status_id=0, area_id=area, price=price, dsp=dsp)

    return '<h>操作成功！请继续。</h>' \
           '<input type="button" name="Submit" onclick="javascript:history.back(-1);" value="返回上一页">'


@DataBase.app.route("/houses", methods=['post'])
def house_operation():
    house_id = request.form.get("buy")
    if house_id is not None:
        print('buy {}'.format(house_id))
        databaseHelper.house_update(house_id=house_id, house_status=1)
        if User.user.type_id == 0:
            return render_template('buy.html', user=User)
        else:
            return render_template('agency.html', user=User)

    house_id = request.form.get("order")
    if house_id is not None:
        databaseHelper.house_update(house_id=house_id, house_status=2)
        databaseHelper.order_insert(userid=User.user.userid, house_id=house_id)
        if User.user.type_id == 0:
            return render_template('buy.html', user=User)
        else:
            return render_template('agency.html', user=User)

    house_id = request.form.get('collection')
    if house_id is not None:
        databaseHelper.collection_insert(userid=User.user.userid, house_id=house_id)
        if User.user.type_id == 0:
            return render_template('buy.html', user=User)
        else:
            return render_template('agency.html', user=User)


@DataBase.app.route("/order", methods=['post'])
def order_operation():
    oid = request.form.get("delete")
    if oid is not None:
        databaseHelper.order_delete(oid=oid)
        if User.user.type_id == 0:
            return render_template('buy.html', user=User)
        else:
            return render_template('agency.html', user=User)
    else:
        print('[Error]: Invalid value for oid')


@DataBase.app.route("/collection", methods=['post'])
def collection_operation():
    cid = request.form.get("delete")
    if cid is not None:
        databaseHelper.collection_delete(cid=cid)
        if User.user.type_id == 0:
            return render_template('buy.html', user=User)
        else:
            return render_template('agency.html', user=User)
    else:
        print('[Error]: Invalid value for cid')


@DataBase.app.route("/agency_buy", methods=['post'])
def agency_buy():
    switch = request.form.get("my-house-list")
    if switch == 'houses':
        houses = databaseHelper.house_query_all()
        return render_template('homePage.html', houses=houses)
    switch = request.form.get("my-order-list")
    if switch == 'orders':
        orders = databaseHelper.order_query_all(User.user.userid)
        print(orders)
        return render_template('orders.html', orders=orders)
    switch = request.form.get("my-collection-list")
    if switch == 'collections':
        collections = databaseHelper.collection_query_all(User.user.userid)
        return render_template('collections.html', collections=collections)

    houseType = request.form.get("houseType")
    houseType_id = houseTypeMapping(houseType)
    area = request.form.get("area")
    area_id = areaMapping(area)
    price = request.form.get("price")

    houses = databaseHelper.house_query(houseType=houseType_id, area=area_id, price=price)
    return render_template('houses.html', houses=houses)


@DataBase.app.route('/agency_sell', methods=['post'])
def agency_sell():
    houseType = houseTypeMapping(request.form.get("houseType"))
    area = areaMapping(request.form.get("area"))
    price = request.form.get("expectedPrice")
    dsp = request.form.get("description")
    databaseHelper.house_insert(type_id=houseType, status_id=0, area_id=area, price=price, dsp=dsp)

    return '<h>操作成功！请继续。</h>' \
           '<input type="button" name="Submit" onclick="javascript:history.back(-1);" value="返回上一页">'


if __name__ == '__main__':
    DataBase.app.run()
