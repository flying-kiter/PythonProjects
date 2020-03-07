# -*- coding: utf-8 -*-
import time  # 导入时间库
import datetime  # 导入日期时间库
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count

"""
1.对比单进程与多进程执行时间
"""


# 定义一个返回日期时间函数
def dt():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 运行函数
def run(v):
    print("{}:[{}]开始运行！".format(dt(), str(v).zfill(2)))
    time.sleep(2)  # 休息2秒
    print("{}:[{}]结束运行！".format(dt(), str(v).zfill(2)))


# 单进程串行方式运行
def single():
    for v in range(0, 16):
        run(v)


# 多进程并行方式运行
def multi():
    # 判断cpu核心数量
    # 根据cpu核心数量来开启多进程
    # 以进程池的方式运行函数
    n = cpu_count()
    # 创建进程池
    p = Pool(n)
    for v in range(0, 16):
        p.apply_async(run, args=(v,))  # 以进程池方式异步运行函数，第一个参数函数名称，args参数元祖
    p.close()  # 关闭进程池
    p.join()  # 等待进程结束


if __name__ == "__main__":
    start_time = time.time()
    # single()
    multi()
    print("总计用时：{}s".format(time.time() - start_time))
