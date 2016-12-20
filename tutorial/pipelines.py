# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from tutorial.items import QuotesItem, AuthorItem

class QuotesPipeline(object):
    authors = set()
    def open_spider(self, spider):
        with open('quotes', 'w') as f:
            f.write('')
        with open('authors', 'w') as f:
            f.write('')
        self.file = open('quotes', 'a')
        self.author = open('authors', 'a')

    def close_spider(self, spider):
        self.file.close()
        self.author.close()

    def process_item(self, item, spider):
        #print(type(item))
        if isinstance(item, AuthorItem):
            if item['name'] in self.authors:
                print(item['name']+' already exists!')
            else:
                self.authors.add(item['name'])
                line = json.dumps(dict(item), ensure_ascii=False) + '\n'
                self.author.write(line)
        else:
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'
            self.file.write(line)
        return item