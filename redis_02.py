from flask import Flask, jsonify, request
import redis
import json
import uuid
import logging#日志
R_conn = redis.Redis(host='localhost', port=6379, db=0)

#全局一次连接，避免重复链接
#日志专业化

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

#将用户的需求解析并加入任务队列
@app.route("/task", methods=["POST"])
def task():


    data = request.json.get("data")
    if not data:
        return jsonify({"code": 400, "msg": "参数错误"}), 400

    #生成任务id
    tid = str(uuid.uuid4())
    #将任务及id先放入字典
    task_dict = {"tid": tid, "data": data}
    logging.info(f"接收到新任务，任务ID: {tid}, 数据: {data}")

    #连接redis


    #将任务字典转化为json字符串，再存入redis队列
    R_conn.lpush("task_queue", json.dumps(task_dict))
    #直接给用户返回任务信息

    return jsonify({"code": 200, "msg": "任务已加入队列", "tid": tid}), 200


#构造一个接口用来查询任务结果
@app.route("/result", methods=["GET"])
def result():
    tid = request.args.get("tid")#获取请求参数
    if not tid:
        return jsonify({"code": 400, "msg": "参数错误"}), 400

    #连接redis，准备查询结果

    result = R_conn.hget("result_dict",tid)#从结果字典中取出结果
    logging.info(f"查询任务结果，任务ID: {tid}")
    if not result:
        return jsonify({"code": 404, "msg": "任务执行中，请稍候再试"}), 404
    #返回结果之前可以考虑将结果从bytes类型转化为字符串类型，并且将任务结果移除完成队列
    R_conn.hdel("result_dict",tid)#将完成的任务从结果字典中移除
    return jsonify({"code": 200, "msg": "任务完成", "result": result.decode("utf-8")}), 200



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
