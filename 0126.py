from flask import Flask,request,jsonify
import os
import pymysql
from dotenv import load_dotenv

load_dotenv()
DB_CONFIG={
    'user':os.getenv("DB_USER"),
    'host':os.getenv("DB_HOST"),
    'password':os.getenv("DB_PASSWORD"),
    'db':os.getenv("DB_NAME"),
    'charset':"utf8mb4",
    'port':3306
}

def conn():
    return pymysql.Connect(**DB_CONFIG,cursorclass=pymysql.cursors.DictCursor)#注意，connect表示去连接，是一个动词，所以用在这里,指定为字典游标
app = Flask(__name__)

@app.route("/login",methods = ['POST'])
def login():
    data = request.get_json()
    username = data.get('name')
    password = data.get('password')
    print(username,password)
    if not username or not password:
        return jsonify({'code':0,'massage':'请输入用户名或者密码'})
    with conn() as connection:
        cur = connection.cursor()
        cur.execute("SELECT * FROM users WHERE name = %s",(username))
        re = cur.fetchall()
        print((re[0])['name'])
    if username == (re[0])['name'] and password == (re[0])['password']:
        return jsonify({'code':1,'massage':'登录成功'})
    else:
        return jsonify({'code':3,'massage':'用户名或密码输入错误，请重试'})


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
















