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
        self.root_url = 'http://www.mafengwo.cn' # 马蜂窝根目录
        self.city_url = 'http://www.mafengwo.cn/mdd/citylist/21536.html?mddid=21536&page={page}' # 马蜂窝中城市目的地页面
        self.guide_url = 'http://www.mafengwo.cn/yj/{city_id}/' # 景点攻略页面
        self.city_page_num = 422
#        self.list_url_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data/list_url.txt') 
        self.list_url_path = '/home/iyuge2/data/mfw/list_url.txt'
        with open(self.list_url_path, 'r', encoding='utf-8') as lf:
            lines = lf.readlines()
            self.list_urls = [line.strip() for line in lines] 

    def get_html(self, url):
        """
        使用request获取一个html
        """
        headers = {
            'User-Agent': random.choice(USER_AGENTS)
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }
        # proxies = {'http:': 'http://' + random.choice(PROXIES)['ip_port'], 'https:': 'https://' + random.choice(PROXIES)['ip_port']}
        # r = requests.get(url, proxies=proxies, headers=headers)
        time.sleep(random.random() + 2.5)
        r = requests.get(url, headers=headers) 
        return r.text

    def start_requests(self):
        """
        指定入口url
        """
        # self.proxy = self.get_proxy()
        # for i in range(0, self.mafengwo_city_page_num):
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
                href = item.find('a', attrs={'data-type': '目的地'})
                try:
                    guide_url = self.guide_url.format(city_id=href['data-id'])
                    if guide_url not in self.list_urls:
                        yield scrapy.Request(url=guide_url, callback=self.parse_guide)
                except:
                    continue

    def parse_guide(self, response):
        """
        爬取攻略信息
        """
        # 解析某页攻略
        soup = BeautifulSoup(response.body, 'html.parser')
        city_name = soup.find('div', attrs={'class': 'crumb'}).find('div', attrs={'class': 'item cur'}).text.strip()[:-2]
        items = soup.find_all('li', attrs={'class': 'post-item'})
        if items:
            for item in items:
                gitem = GuideItem()
                # 地点
                gitem['city_name'] = city_name
                # 图片地址
                try:
                    gitem['cover_img_url'] = item.find('img', attrs={'class': 'lazy'})['data-original']
                except:
                    gitem['cover_img_url'] = ''
                try:
                    # 标题和链接
                    title = item.find('a', attrs={'class': 'title-link'})
                    gitem['title'] = title.text.strip()
                    gitem['guide_url'] = self.root_url + title['href']
                    # 作者和作者链接
                    author = item.find('span', attrs={'class': 'author'}).find_all('a')[-1]
                    gitem['author'] = author.text.strip()
                    gitem['author_url'] = self.root_url + author['href']
                except:
                    continue
                # 概要
                try:
                    gitem['outline'] = item.find('div', attrs={'class': 'post-content'}).text.strip()
                except:
                    gitem['outline'] = ''
                # 观看人数
                try:
                    gitem['view'] = item.find('span', attrs={'class': 'status'}).contents[1]
                except:
                    gitem['view'] = '0'
                # 进入攻略详情，查看出行天数和出行日期
                gitem['date'], gitem['days'] =  self.get_days_date(gitem['guide_url'])
                yield gitem
            with open(self.list_url_path, 'a', encoding='utf-8') as df:
                df.write(response.url+'\n')
                self.list_urls.append(response.url)
        # 找到下一页标签
        try:
            pagebar = soup.find('div', attrs={'class': '_pagebar'})
            next_url = self.root_url + pagebar.find('a', attrs={'class': 'ti next'})['href']
            if next_url not in self.list_urls:
                yield scrapy.Request(url=next_url, callback=self.parse_guide)
        except:
            return
    
    def get_days_date(self, url):
        """
        获取攻略信息中的出发时间和旅游天数
        """
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        try:
            tt = soup.find('div', attrs={'class':'tarvel_dir_list'})
            # 获取时间
            t_time = tt.find('li', attrs={'class':'time'}).text
            date = t_time[t_time.find(r'/')+1:]
            # 获取天数
            d_time = tt.find('li', attrs={'class':'day'}).text
            day = d_time[d_time.find(r'/')+1:]
            return date, day
        except:
            try:
                tt = soup.find('div', attrs={'class':'vc_time'})
                t_time = tt.find('span', attrs={'class': 'time'}).text
                date = t_time.split()[0]
                return date, '0天'
            except:
                return '1972-01-01', '-1天'
        
