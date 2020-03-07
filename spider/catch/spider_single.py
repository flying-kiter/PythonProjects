# -*- coding: utf-8 -*-
import os  # 导入文件目录操作库
import datetime  # 导入日期时间库
import requests  # 导入http客户端库

"""
1.requests http 客户端请求库怎么用？
以百度：http://www.baidu.com为例
url = "http://www.baidu.com"

# 定义请求，请求结果赋值响应对象
# method：请求方法
# url：请求地址
response = requests.request(method="GET", url=url)
print(response)  # 打印响应对象
print(dir(response))  # 响应对象可以调用的属性和方法
# response.text # 响应的内容
print(response.text)
# response.encoding # 响应的字符集
print(response.encoding)
# response.headers # 响应的头信息
print(response.headers)
# response.status_code # 响应的状态码
print(response.status_code)
# response.cookies # 响应的会话信息
print(response.cookies)

# 怎么把响应内容里面的乱码转化为正常字符
response.encoding = "utf-8"
print(response.text)
"""

"""
2.封装单进程爬虫
"""


class SpiderSingle(object):
    # 定义一个初始化的构造方法
    # 1.urls地址生成器，2.保存html目录
    def __init__(self, urls, path):
        self.urls = urls  # 把urls赋值给self.urls这个实例属性
        self.path = path  # 把path赋值给self.path这个实例属性

    # 创建打印日志方法
    def log(self, url, save_path):
        # %Y：年，%m：月，%d：日，%H：时，%M：分，%S：秒
        print("{dt}:{url}->{save_path}".format(
            dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            url=url,
            save_path=save_path
        ))

    # 单进程爬取页面的逻辑
    def catch_pages(self):
        # 1.定义请求的生成器
        resps = (
            requests.request(method="GET", url=url) for url in self.urls
        )

        # 2.判断并创建保存html的路径
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        # 3.迭代请求生成器，把响应内容保存到html中，再把html保存到保存目录中去
        n = 1
        for resp in resps:
            resp.encoding = "utf-8"  # 设置响应内容的编码utf-8
            save_path = os.path.join(
                self.path,
                "{}.html".format(
                    n
                )
            )  # 拼接保存目录路径和html名称
            # 以写的方式，字符集utf-8打开html
            with open(save_path, "w", encoding="utf-8") as f:
                # 写入响应内容
                f.write(resp.text)
            self.log(resp.url, save_path)
            n += 1  # 每次循环迭代的时候，n自增1
