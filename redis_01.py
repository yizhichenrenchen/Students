#导入所需模块
from flask import Flask,request,jsonify
import os
import pymysql
from dotenv import load_dotenv
from dbutils.pooled_db import PooledDB
import redis
import uuid
import json




app = Flask(__name__)

@app.route("/task",methods = ['POST'])#绑定路由
def task():
    ordered_string = request.json.get("ordered_string")#获取前端传来的json数据
    if not ordered_string:
        return jsonify({"code":400,"msg":"参数错误"}),400#简单判断有无传入数据
    #生成任务id
    tid = str(uuid.uuid4())
    #将任务加入队列，
    task_dict = {"tid":tid,"ordered_string":ordered_string}#将id与用户输入的字符串整合为字典
    #连接redis
    Redis_conn = redis.Redis(host='localhost', port=6379, db=0)
    #这里在redis中创建了一个splider_task_list这个列表，用来存放任务字典
    Redis_conn.lpush("splider_task_list",json.dumps(task_dict))#将任务字典转化为json字符串，再存入redis队列
    return jsonify({"code":200,"msg":"任务提交成功","tid":tid}),200#返回任务id





if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
















