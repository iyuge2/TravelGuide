## 旅游攻略爬虫

- requirements
```
python==3.7.3
elasticsearch==7.0.0
requests==2.20.0
Scrapy==1.6.0
beautifulsoup4==4.7.
```

> 使用`scrapy`爬取了[马蜂窝](http://www.mafengwo.cn)和[去哪儿网](https://travel.qunar.com)的旅游攻略,得到的html文件通过`beautifulsoup`进行解析,解析完的数据存在`elasticsearch`数据库中，同时存有一份文本备份。

- 如何运行？
```
cd mafengwo 或者 cd qunaer
scrapy crawl TravelGuide
```

PS: 由于**懒**，没有通过模块化将两份代码合并在一起。