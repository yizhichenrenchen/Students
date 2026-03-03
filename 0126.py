#导入所需模块
from flask import Flask,request,jsonify
import os
import pymysql
from dotenv import load_dotenv
from dbutils.pooled_db import PooledDB


#加载环境变量
load_dotenv()
#数据库配置
DB_CONFIG={
    'user':os.getenv("DB_USER"),
    'host':os.getenv("DB_HOST"),
    'password':os.getenv("DB_PASSWORD"),
    'db':os.getenv("DB_NAME"),
    'charset':"utf8mb4",
    'port':3306
}

POOL = PooledDB(
    creator=pymysql,#使用链接数据库的模块
    maxconnections=10,#连接池允许的最大连接数量
    mincached=2,#初始连接池创建连接数量
    maxcached=5,#闲置连接的最大数量
    blocking=True,#无可用链接时是否阻塞等待，是Ture，否False，不等待报错
    setsession=[],#开始会话前执行的命令列表
    ping=0,
    **DB_CONFIG,
    cursorclass=pymysql.cursors.DictCursor#指定连接的游标类型，这里为字典类型
)

#连接数据库函数，返回一个连接对象
def conn():
    return POOL.connection()#注意，connect表示去连接，是一个动词，所以用在这里,指定为字典游标
app = Flask(__name__)

@app.route("/login",methods = ['POST'])#绑定路由
def login():#路由函数，实现登录功能
    data = request.get_json()#获取请求数据
    username = data.get('name')#获取用户名
    password = data.get('password')#获取密码
    print(username,password)
    if not username or not password:#判断是否输入用户名和密码
        return jsonify({'code':0,'massage':'请输入用户名或者密码'}),201
    with conn() as connection:#使用with语句，自动关闭数据库连接
        cur = connection.cursor()#创建游标
        cur.execute("SELECT * FROM users WHERE name = %s",(username))#执行sql语句，查询用户名是否存在，并使用占位符防止sql注入
        re = cur.fetchall()
        print(re)#获取查询结果
        print((re[0])['name'])
    if username == (re[0])['name'] and password == (re[0])['password']:
        return jsonify({'code':1,'massage':'登录成功'}),200
    else:
        return jsonify({'code':3,'massage':'用户名或密码输入错误，请重试'}),401
@app.route("/register",methods = ['POST'])#绑定路由
def register():
    data = request.get_json()#获取请求数据
    username = data.get('name')#获取用户名
    password = data.get('password')#获取密码
    print(username,password)
    if not username or not password:#判断是否输入用户名和密码
        return jsonify({'code':0,'massage':'请输入用户名或者密码'}),201
    with conn() as connection:
        cur = connection.cursor()
        cur.execute("INSERT INTO users(name,password) VALUES(%s,%s)",(username,password))
        connection.commit()
        print(f"注册成功，用户名：{username}")
        return jsonify({"code":4,"massage":"注册成功"}),200


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
















