# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class GuideItem(Item):
    # define the fields for your item here like:
    # 城市id
    city_name = Field()
    # 标题
    title = Field()
    # 作者
    author = Field()
    # 作者url(不一定有,没有的话为空)
    author_url = Field()
    # 观看人数
    view = Field()
    # 攻略概要
    outline = Field()
    # 攻略链接
    guide_url = Field()
    # 封面
    cover_img_url = Field()
    # 出行天数
    days = Field()
    # 日期(2008-08-08)
    date = Field()