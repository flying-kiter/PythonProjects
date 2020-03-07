# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base  # 用来创建模型继承父类
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, DECIMAL, DATETIME  # 大整型,变长字符串类型,浮点型,日期时间类型
from sqlalchemy import Column  # 用来创建模型的字段

# from models.configs import mysql_configs  # 导入mysql连接配置

# 定义父类
Base = declarative_base()

# 创建元类
metadata = Base.metadata

"""
设计bootstrap主题产品模型
分析字段：
    1.编号，id，大整型，主键，自动递增
    2.标题，title，字符串，非空
    3.封面，logo，字符串，非空
    4.详情地址，url，字符串，非空
    5.预览地址，preview，字符串，非空
    6.分类，cate，字符串，非空
    7.价格，price，浮点型，非空
    8.保存时间，createdAt，日期时间，非空
    9.修改时间，updatedAt，日期时间，非空
"""


# 创建模型
class BsThemeProduct(Base):
    # 指定数据表原始名称
    __tablename__ = "bs_theme_product"
    id = Column(BIGINT, primary_key=True)  # 编号
    title = Column(VARCHAR(255), nullable=False)  # 标题
    logo = Column(VARCHAR(255), nullable=False)  # 封面
    url = Column(VARCHAR(255), nullable=False)  # 详情地址
    preview = Column(VARCHAR(255), nullable=False)  # 预览地址
    cate = Column(VARCHAR(100), nullable=False)  # 分类
    price = Column(DECIMAL(6, 2), nullable=False)  # 价格
    createdAt = Column(DATETIME, nullable=False)  # 保存时间
    updatedAt = Column(DATETIME, nullable=False)  # 修改时间


# 如果程序结构等于自己
if __name__ == "__main__":
    import mysql.connector  # 导入数据库连接驱动
    from sqlalchemy import create_engine  # 导入创建连接引擎函数

    # 创建连接引擎
    """
    数据库配置
    db_host：主机名称
    db_port：端口
    db_user：用户名
    db_pwd：密码
    db_name：数据库名称

    创建引擎
    第一项参数：连接字符串
    encoding：编码
    echo：是否输出日志，True输出，False不输出
    """
    mysql_configs = dict(
        db_host="127.0.0.1",
        db_port=3306,
        db_user="root",
        db_pwd="lxh530672zxc",
        db_name="spider_data"
    )

    engine = create_engine(
        "mysql+mysqlconnector://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}".format(
            **mysql_configs
        ),
        encoding="utf-8",
        echo=True
    )
    # 将模型生成数据表
    metadata.create_all(engine)
    print("************恭喜你，创建成功！************")
