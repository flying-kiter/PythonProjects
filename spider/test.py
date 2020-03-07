# -*- coding: utf-8 -*-
from lxml import etree  # 节点树库

# 打开html，读取html内容
with open("test.html", "r", encoding="utf-8") as f:
    html = f.read()
    selector = etree.HTML(html)
    print(selector)
    """
    提取标题
    提取关键字
    提取介绍
    提取链接地址
    提取图片地址
    提取文本内容

    xpath路径语法
    //忽略上级节点
    text()：获取标签包裹的内容
    @属性名称：获取属性内容
    """
    title = selector.xpath('//title/text()')[0]
    keywords = selector.xpath('//meta[@name="keywords"]/@content')[0]
    description = selector.xpath('//meta[@name="description"]/@content')[0]
    a = selector.xpath('//div[@id="abc"]/div[@class="efg"]/a/@href')[0]
    img = selector.xpath('//div[@id="abc"]/div[@class="efg"]/img/@src')[0]
    p = selector.xpath('//div[@id="abc"]/div[@class="efg"]/p/text()')[0]
    print(title)
    print(keywords)
    print(description)
    print(a)
    print(img)
    print(p)