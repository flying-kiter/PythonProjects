# -*- coding: utf-8 -*-
import os
import requests
from catch.spider_single import SpiderSingle
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count


# 多进程爬虫类
class SpiderMulti(SpiderSingle):
    # 执行请求的方法
    def catch_page_process(self, url, n):
        # 1.定义请求响应对象
        resp = requests.request(method="GET", url=url)

        # 2.判断创建保存目录
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        # 3.保存抓取响应内容
        resp.encoding = "utf-8"
        save_path = os.path.join(self.path, "{}.html".format(n))
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(resp.text)
        # 4.输出抓取日志
        self.log(resp.url, save_path)

    # 多进程的方法
    def catch_pages(self):
        cpu_num = cpu_count()  # 获取cpu数量
        p = Pool(cpu_num)  # 定义进程池
        n = 1
        for url in self.urls:
            p.apply_async(self.catch_page_process, args=(url, n))  # 以进程池的方式运行请求方法
            n += 1
        p.close()  # 关闭
        p.join()  # 等待
