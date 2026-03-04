import redis
import json
import hashlib
def get_task():#取出任务
    Redis_conn = redis.Redis(host='localhost', port=6379, db=0)#数据库连接
    data = Redis_conn.brpop("splider_task_list", timeout=10)#从Redis队列右边取出一个任务装进变量data中，一直执行这个动作，timeout表示等待10秒
    if not data:#判断是否有任务，没有直接返回
        return
    #这里返回解析后的数据，因为取出之后的东西实际上为一个两个元素的元组，所以通过索引取出值并通过decode属性来指定具体类型，
    return json.loads(data[1].decode('utf-8'))


def set_result(tid,value):#此处为构造一个任务执行情况字典
    Redis_conn = redis.Redis(host='localhost', port=6379, db=0)#连接
    Redis_conn.hset("splider_result_dict",tid,value)#将生成的任务id以及算法生成的sign装进构造好的字典


def run():
    while True:#死循环，一直获取任务
        #获取任务
        task_dict = get_task()#将前面函数返回的值赋值给变量
        print(task_dict)
        if not task_dict:#判断有没有任务
            print("没有任务了，等待10秒后继续检查")
            continue
            #brpop命令表示从队列右边取出一个任务字典，如果队列为空则阻塞等待
            #实现签名算法
        ordered_string = task_dict['ordered_string']
        encrypt_string = ordered_string + "566546546464684848484844wd5w4"
        obj = hashlib.md5(encrypt_string.encode('utf-8'))
        sign = obj.hexdigest()


        tid = task_dict['tid']
        set_result(tid,sign)





if __name__ == '__main__':
    run()
