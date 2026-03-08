import redis
import json
import logging
import docx
import document
R_conn = redis.Redis(host='localhost', port=6379, db=0)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#获取任务函数
def get_task():
    #连接redis

    #从redis队列右边取出一个任务，阻塞等待10秒
    data = R_conn.brpop("task_queue", timeout=10)
    if not data:
        return None#注意此处实际上为一个两个元素的元组，我们需要通过索引取出值并通过decode属性来指定具体类型

    logging.info(f"从队列中取出任务，任务内容: {data}")

    logging.info(f"转化编码类型，任务内容: {data[1].decode('utf-8')}")

    logging.info(f"解析任务内容，任务内容: {json.loads(data[1].decode('utf-8'))}, 数据类型: {type(json.loads(data[1].decode('utf-8')))}")
    #返回任务内容

    return json.loads(data[1].decode("utf-8"))


#存储结果函数
def set_result(tid, value):
    #连接redis

    #将生成的任务id以及算法生成的结果装进一个字典中
    R_conn.hset("result_dict", tid, value)

key_type = R_conn.type("result_dict")
logging.info(f"结果队列数据类型为 {key_type}")



def run():
    while True:
        task = get_task()
        #判断有无任务可处理，无则跳过本次循环
        if not task:
            print("等待中...")
            continue
        print("开始处理任务：", task)

        #处理任务
        data = task["data"]
        result = data + "室分需求导入"
        #至此主要算法完成，应该考虑将完成的任务存入一个队列中，或者存入一个字典中以便后续查询，本处考虑将结果存入一个字典中，键为任务id，值为结果
        tid = task["tid"]
        set_result(tid, result)
        print("任务完成，结果已存储")








if __name__ == '__main__':
    run()
