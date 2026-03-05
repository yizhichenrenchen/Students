import redis
import json

key_name = "result_dict"
R_conn = redis.Redis(host='localhost', port=6379, db=0)
key_type = R_conn.type("result_dict")
R_conn.delete(key_name)
print(f"已清除旧数据 {key_name}，准备重新初始化...")

#获取任务函数
def get_task():
    #连接redis
    R_conn = redis.Redis(host='localhost', port=6379, db=0)
    #从redis队列右边取出一个任务，阻塞等待10秒
    data = R_conn.brpop("task_queue", timeout=10)
    if not data:
        return None#注意此处实际上为一个两个元素的元组，我们需要通过索引取出值并通过decode属性来指定具体类型
    print(data)
    print(type(data[1].decode("utf-8")), data[1].decode("utf-8"))
    print(type(json.loads(data[1].decode("utf-8"))), json.loads(data[1].decode("utf-8")))
    #返回任务内容

    return json.loads(data[1].decode("utf-8"))


#存储结果函数
def set_result(tid, value):
    #连接redis
    R_conn = redis.Redis(host='localhost', port=6379, db=0)
    #将生成的任务id以及算法生成的结果装进一个字典中
    R_conn.hset("result_dict", tid, value)

key_type = R_conn.type("result_dict")
print(f"数据类型为 {key_type}")



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
        result = data + " processed"
        #至此主要算法完成，应该考虑将完成的任务存入一个队列中，或者存入一个字典中以便后续查询，本处考虑将结果存入一个字典中，键为任务id，值为结果
        tid = task["tid"]
        set_result(tid, result)
        print("任务完成，结果已存储")








if __name__ == '__main__':
    run()
