from elasticsearch import Elasticsearch

es = Elasticsearch()

item_dict = {'author': '小鹿斑比',
            'author_url': 'http://www.mafengwo.cn/u/64231691.html',
            'cover_img_url': 'http://b2-q.mafengwo.net/s13/M00/31/A2/wKgEaVyy9YuAZ6_BAAUODNVEVFM64.jpeg',
            'date': '1972-01-01',
            'days': '0天',
            'guide_url': 'http://www.mafengwo.cn/i/12361478.html',
            'outline': '三月  ▏春天的季节\n'
                        '那次谁碰上了谁 雨带雷雨伞破损 我与谁脸上滴雨水\n'
                        '我笑言雨快要停 却错失不闻不问哪是谁 转身去\n'
                        '\n'
                        '春天 ▏跟着春天的步伐去寻味美食\n'
                        '201...',
            'title': '·八天七夜广州顺德寻味美食之旅',
            'view': '559'}
a = es.index(index='guide', doc_type='guide', body=item_dict)

print(a)