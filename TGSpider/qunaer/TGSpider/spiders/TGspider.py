import os
import requests
import scrapy
import random
import time
from bs4 import BeautifulSoup
from TGSpider.items import GuideItem
# from TGSpider.settings import USER_AGENTS, PROXIES
from TGSpider.settings import USER_AGENTS

class TGSpider(scrapy.Spider):
    name = 'TravelGuide'

    def __init__(self):
        self.root_url = 'https://travel.qunar.com'
        self.city_url = 'https://travel.qunar.com/p-sx{page}?area=1' # 城市目的地页面
        self.city_page_num = 213
        # self.list_url_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data/list_url.txt')
        self.list_url_path = '/home/iyuge2/data/qne/list_url.txt'

        with open(self.list_url_path, 'r', encoding='utf-8') as lf:
            lines = lf.readlines()
            self.list_urls = [line.strip() for line in lines] 

    def start_requests(self):
        """
        指定入口url
        """
        for i in range(0, self.city_page_num):
            cur_url = self.city_url.format(page=i+1)
            yield scrapy.Request(url=cur_url, callback=self.parse_city) # 指定使用self.parse解析爬取到的网页

    def parse_city(self, response):
        """
        爬取城市列表，或者每个城市的攻略界面url
        response.url
        """
        # 解析网页得到城市信息
        soup = BeautifulSoup(response.body, 'html.parser')
        items = soup.find_all('li', attrs={'class': 'item'})
        if items:
            for item in items:
                cur_guide_url = item.find('a', attrs={'class': 'imglink'})
                if cur_guide_url:
                    yield scrapy.Request(url=cur_guide_url['href'], callback=self.parse_guide)

    def parse_guide(self, response):
        """
        爬取攻略信息
        """
        # 解析某页攻略
        soup = BeautifulSoup(response.body, 'html.parser')
        city_name = soup.find('h1', attrs={'class': 'tit'}).text.strip()
        items = soup.find_all('li', attrs={'class': 'list_item'})
        if response.url not in self.list_urls:
            if items:
                for item in items:
                    gitem = GuideItem()
                    # 地点
                    gitem['city_name'] = city_name
                    # 图片地址
                    try:
                        pic = item.find('li', attrs={'class': 'pic'})
                        gitem['cover_img_url'] = pic.find('img')['src']
                    except:
                        gitem['cover_img_url'] = ''
                    try:
                        # 标题和链接
                        title = item.find('h3', attrs={'class': 'tit'}).find('a')
                        gitem['title'] = title.text.strip()
                        gitem['guide_url'] = title['href']
                        # 作者信息
                        user_info = item.find('p', attrs={'class': 'user_info'})
                        author = user_info.find('span', attrs={'class': 'user_name'}).find('a')
                        gitem['author'] = author.text.strip()
                        gitem['author_url'] = author['href']
                    except:
                        continue
                    try:
                        gitem['date'] = user_info.find('span', attrs={'class': 'date'}).text.strip()
                    except:
                        gitem['date'] = '1972-01-01'
                    try:
                        gitem['days'] = user_info.find('span', attrs={'class': 'days'}).text.strip()
                    except:
                        gitem['days'] = '共-1天'
                    # 观看人数
                    try:
                        gitem['view'] = user_info.find('span', attrs={'class': 'icon_view'}).text.strip()
                    except:
                        gitem['view'] = '0'
                    # 概要
                    try:
                        places = item.find_all('p', attrs={'class': 'places'})
                        gitem['outline'] = places[len(places)-1].text.strip()
                    except:
                        gitem['outline'] = ''
                    yield gitem
            with open(self.list_url_path, 'a', encoding='utf-8') as df:
                df.write(response.url+'\n')
                self.list_urls.append(response.url)
        # 找到下一页标签
        try:
            next_url = soup.find('a', attrs={'class': 'page next'})['href']
            if next_url not in self.list_urls:
                yield scrapy.Request(url=next_url, callback=self.parse_guide)
        except:
            return
            
