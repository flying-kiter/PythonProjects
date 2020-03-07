# -*- coding: utf-8 -*-
import os
import datetime
import mysql.connector
from lxml import etree
from models.configs import mysql_configs
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker  # 会话创建工具
from models.models import BsThemeProduct  # 导入模型


class PickSave:
    # 定义初始化构造方法
    def __init__(self, path):
        self.path = path  # 把路径赋值实例属性self.path
        self.db = self.session

    # 定义连接会话
    @property
    def session(self):
        # 创建连接引擎
        engine = create_engine(
            'mysql+mysqlconnector://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'.format(
                **mysql_configs
            ),
            encoding="utf-8",
            echo=True,
            pool_size=100,
            pool_recycle=10,
            connect_args={'charset': 'utf8'}
        )  # pool_size：连接池大小；pool_recycle：连接池生命周期；connect_args：连接选项
        # 定义会话
        Session = sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=True,
            expire_on_commit=False
        )  # bind绑定连接引擎；autocommit：True自动提交，False事务提交；autoflush：True自动刷新权限，False不自动；expire_on_commit：True自动提交，False事务提交
        return Session()

    # 解析数据
    def pick(self):
        # 1.获取抓取所有的html
        html_list = os.listdir(self.path)
        # print(html_list)
        data = []
        # 2.拼接路径和html
        for html in html_list:
            html_path = os.path.join(self.path, html)
            # print(html_path)
            # 3.打开html
            with open(html_path, "r", encoding="utf-8") as f:
                # print(f.read())
                # 把html内容转化为节点选择器
                selector = etree.HTML(f.read())
                # print(selector)
                # 定义细胞选择器
                items = selector.xpath('//div[@id="content"]/ul/li/div')
                # print(items)
                for item in items:
                    data.append(
                        dict(
                            title=str(item.xpath('div[2]/div[1]/a/text()')[0]),
                            logo=str(item.xpath('div[1]/a[1]/img/@src')[0]),
                            url=str(item.xpath('div[1]/a[1]/@href')[0]),
                            preview=str(item.xpath('div[1]/a[2]/@href')[0]),
                            cate=str(item.xpath('div[2]/div[1]/ul/li/a/text()')[0]),
                            price=float(item.xpath('div[2]/div[2]/p/span/text()')[0])
                        )
                    )
        return data

    @property
    def dt(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 保存数据
    def save(self):
        # 事务处理的逻辑
        try:
            # 执行代码块
            # 获取数据
            data = self.pick()
            for v in data:
                cd = dict(
                    createdAt=self.dt,
                    updatedAt=self.dt,
                    **v
                )
                bs_theme_product = BsThemeProduct(
                    **cd
                )
                # print(bs_theme_product)
                self.db.add(bs_theme_product)  # 添加数据至数据库中
        except Exception as e:
            # print(e)
            # 出现异常代码块
            self.db.rollback()  # 回滚
        else:
            # 没有出现异常代码块
            self.db.commit()  # 提交
        finally:
            # 无论是否发送异常都执行的代码块
            self.db.close()  # 关闭会话
