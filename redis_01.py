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
    #redis任务队列一般为左进右出，即新任务加入到队列左边，旧的任务从右边开始删除或者取出，所以这里不需要删除任务
    #lpush命令表示将任务字典存入队列左边，rpush命令表示将任务字典存入队列右边
    return jsonify({"code":200,"msg":"任务提交成功","tid":tid}),200#返回任务id

@app.route("/result",methods = ['GET'])
def result():
    tid = request.args.get("tid")#获取get请求传过来的tid参数
    Redis_conn = redis.Redis(host='localhost', port=6379, db=0)
    if not tid:#判断有无传入参数
        return jsonify({"code":400,"msg":"参数错误"}),400
    sign = Redis_conn.hget("splider_result_dict",tid)#查询是否已经完成任务加入到完成队列中
    if not sign:
        return jsonify({"code":200,"msg":"执行中，请继续等待","tid":tid}),200
    #此时已经可以返回sign签名，但是此时sign值为字节类型，首先需要转换
    sign_string = sign.decode('utf-8')
    #然后给用户返回
    #但是在这时候，只是进行了查询，并没有将完成的任务从已完成的队列中移除，应该要移除，所以要移除之后在返回
    Redis_conn.hdel("splider_result_dict",tid)
    return jsonify({"code":200,"msg":"已完成","data":sign_string}),200







if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
















