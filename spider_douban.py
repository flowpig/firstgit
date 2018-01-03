#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from requests.exceptions import RequestException
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import re
import json
import codecs


def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile(
        r'<div class="item">.*?<em class="">(?P<id>.*?)</em>.*?<span class="title">(?P<title>.*?)</span>'
        + '.*?<p class="">.*?导演:(?P<director>.*?)&nbsp.*?</p>.*?<span class="rating_num".*?>(?P<num>.*?)</span>.*?<span>(?P<comment>.*?)人评价</span>',re.S
    )
    items = re.finditer(pattern,html)
    for item in items:
        yield item
    # return items
    # for item in items:
    #     print(item.group('id', 'title', 'director', 'num', 'comment'))

def write_to_file(content):
    with open('douban_top250','a',encoding='utf-8-sig') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
        f.close()

def spider_crawl(page):
    url = 'https://movie.douban.com/top250?start={page}&filter='.format(page=page*25)
    html = get_one_page(url)
    items = parse_one_page(html)
    title = ('排名', '电影名', '导演', '评分', '评价人')
    for item in items:
        content = dict(zip(title, item.group('id', 'title', 'director', 'num', 'comment')))
        print(content)
        write_to_file(content)

if __name__ == '__main__':
    pool = ProcessPoolExecutor()
    pool.map(spider_crawl,[i for i in range(10)])