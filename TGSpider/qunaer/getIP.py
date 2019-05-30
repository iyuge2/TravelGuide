import os
import requests
import time
from bs4 import BeautifulSoup

cur_dir = os.path.dirname(os.path.abspath(__file__))

fetch_times = 15 # 爬取几次，每次可获得15条ip(可能有重复)
stop_time = 12 # 每隔12s爬取一次
all_ips = [] # 防止加入重复ip

with open(os.path.join(cur_dir, 'ips.txt'), 'w', encoding='utf-8') as ipf:
    for i in range(0,fetch_times):
        r = requests.get('http://ip.jiangxianli.com/')
        soup = BeautifulSoup(r.text, 'html.parser')

        ips = soup.find_all('button', attrs={'class': 'btn'})

        for ip in ips:
            cur_ip = ip['data-url']
            pos = cur_ip.find('/') + 2
            cur_ip = cur_ip[pos:]
            if cur_ip not in all_ips:
                ipf.write("{{'ip_port': '{0}', 'user_pass': ''}},\n".format(cur_ip))
            all_ips.append(cur_ip)

        time.sleep(stop_time) 