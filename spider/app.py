# -*- coding: utf-8 -*-
import os  # 导入文件目录操作
from catch.spider_single import SpiderSingle  # 导入单进程爬虫类
from catch.spider_multi import SpiderMulti  # 导入多进程爬虫类
from pick.pick_save import PickSave  # 导入提取保存类
from pprint import pprint

if __name__ == "__main__":
    # 定义请求地址生成器
    urls = (
        "https://themes.getbootstrap.com/shop/page/{}/?orderby=popularity".format(v)
        for v in range(1, 5)
    )
    # 定义保存的路径，os.path.dirname(__file__)：获取当前脚本所在的路径
    path = os.path.join(
        os.path.dirname(__file__),
        "result/bs_theme_product"
    )
    # s = SpiderSingle(urls, path)  # 实例化单进程爬虫类
    # s.catch_pages()  # 执行单进程抓取页面
    m = SpiderMulti(urls, path)  # 实例化多进程爬虫类
    m.catch_pages()  # 执行多进程抓取页面
    print("----------------------------")
    ps = PickSave(path)  # 实例化类
    # pprint(ps.pick()) # 提取数据
    ps.save()  # 保存数据
