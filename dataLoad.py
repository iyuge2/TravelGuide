import os
import ast
import json
from tqdm import tqdm
from elasticsearch import Elasticsearch

es = Elasticsearch()
# 删除已有索引
es.indices.delete(index='travelguide', ignore=[400, 404])
# 增加索引
es.indices.create(index='travelguide', ignore=400)


with open('data_clean/guide_mfw_v1.txt', 'r', encoding='utf-8') as gf:
    lines = gf.readlines()
    for line in tqdm(lines):
        item_dict = ast.literal_eval(line)
        item_dict['view'] = int(item_dict['view'])
        item_dict['days'] = int(item_dict['days'][:-1])
        es.index(index='travelguide', doc_type='guide', body=item_dict)

with open('data_clean/guide_qne_v1.txt', 'r', encoding='utf-8') as gf:
    lines = gf.readlines()
    for line in tqdm(lines):
        item_dict = ast.literal_eval(line)
        item_dict['date'] = item_dict['date'].split()[0]
        view = item_dict['view'][1:]
        if view[-1] == '万':
            item_dict['view'] = int(float(view[:-1])*10000)
        else:
            item_dict['view'] = int(view)
        item_dict['days'] = int(item_dict['days'][1:-1])
        es.index(index='travelguide', doc_type='guide', body=item_dict)
