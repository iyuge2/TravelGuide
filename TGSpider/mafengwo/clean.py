import os
from elasticsearch import Elasticsearch

es = Elasticsearch()
# 删除已有索引
es.indices.delete(index='mfw_guide', ignore=[400, 404])
# 增加索引
es.indices.create(index='mfw_guide', ignore=400)

#cur_path = os.path.dirname(os.path.abspath(__file__))
#with open(os.path.join(cur_path, 'data/guide.txt'), 'w'):
#    pass
#with open(os.path.join(cur_path, 'data/list_url.txt'), 'w'):
#    pass
cur_path = '/home/iyuge2'
with open(os.path.join(cur_path, 'data/mfw/guide.txt'), 'w'):
    pass
with open(os.path.join(cur_path, 'data/mfw/list_url.txt'), 'w'):
    pass
