# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
from elasticsearch import Elasticsearch

class TgspiderPipeline(object):
    def __init__(self):
#        cur_path = os.path.dirname(os.path.abspath(__file__))
#        self.guide_json_file = os.path.join(cur_path, '../data/guide.txt')
        self.guide_json_file = '/home/iyuge2/data/qne/guide.txt'
        self.es = Elasticsearch()

    def process_item(self, item, spider):
        item_dict = item._values
        self.es.index(index='qne_guide', doc_type='qne_guide', body=item_dict)
        with open(self.guide_json_file, 'a', encoding='utf-8') as tf:
            tf.write(str(item_dict)+'\n')
