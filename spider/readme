# 1.确定程序结构

>--- app.py #入口启动脚本【执行抓取任务、执行保存任务、执行解析任务、执行存入数据表任务】
>---- models #模型包【存放模型】
>-------- models.py #模型模块【存放模板信息模型】
>-------- configs.py #数据库连接配置
>---- catch #爬虫包【单进程抓取模块、多进程抓取模块】
>-------- spider_single.py #单进程抓取模块
>-------- spider_mutil.py #多进程抓取模块
>-------- single_mutil.py #单进程多进程对比
>---- pick #提取保存包【存放提取保存的模块】
>-------- pick_save.py #提取保存模块
>---- result #存放抓取数据的目录
>-------- bs_theme #存放指定网站数据的目录

# 2.设计数据表
## 2-1.确定数据库名称
    ### 如果不存在则创建
    _create database if not exists spider;_
    ## 如果存在则删除
    _drop database if exists spider;_
    ### 切换到爬虫数据库中
    _use spider;_
## 2-2.确定数据表
    ###分析字段：
        1. 编号，id，大整型，主键，自动递增
        2. 标题，title，字符串，非空
        3. 封面，logo，字符串，非空
        4. 详情地址，url，字符串，非空
        5. 预览地址，preview，字符串，非空
        6. 分类，cate，字符串，非空
        7. 价格，price，浮点型，非空
        8. 保存时间，createdAt，日期时间，非空
        9. 修改时间，updatedAt，日期时间，非空
## 2-2.通过mysql原生语法设计
    ### 如果不存在则创建
    ```python
        create table if not exists bs_theme_product(
        id bigint auto_increment key comment "编号",
        title varchar(255) not null comment "标题",
        logo varchar(255) not null comment "封面",
        url varchar(255) not null comment "详情地址",
        preview varchar(255) not null comment "预览地址",
        cate varchar(100) not null comment "分类",
        price decimal(6,2) not null comment "价格",
        createdAt datetime not null comment "保存时间",
        updatedAt datetime not null comment "修改时间"
    )engine=InnoDB charset=utf8 comment "bootstrap主题产品表";
    ```
## 2-3.通过python sqlalchemy orm对象关系映射模型设计
    ###见models/models.py代码

# 3.编写单进程爬虫
    >3-1.定义请求的生成器
    >3-2.判断保存目录是否存在，不存在则创建
    >3-3.迭代生成器，要把响应的信息保存到html文件中，将html文件保存至保存目录中

# 4.多进程爬虫
    >4-1.怎么使用多进程
    >4-2.使用多进程编写爬虫

# 5.提取html节点的内容
    >5-1.怎么使用lxml
    >5-2.使用lxml提取result/bs_theme_product