# https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?symbol=600000&t1=all&p=1
import requests
from lxml import etree
import json
import csv
import random
import redis
import fake_useragent
ua = fake_useragent.UserAgent()


# 返回单页面所有url
def getProxy():
    # 连接到本地Redis数据库
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    # 获取所有键名为"use_proxy"的键的值
    all_values = redis_client.hvals('use_proxy')
    # 从值中筛选出"last_status": true的键
    filtered_keys = []
    for value in all_values:
        data = json.loads(value.decode('utf-8'))
        if data.get('last_status') is True:
            filtered_keys.append(data)
    # 从筛选后的键中随机选择一个键
    proxy = random.choice(filtered_keys)['proxy']
    # print(proxy)
    proxies = {'http': f'http://{proxy}', 'https': f'https://{proxy}'}
    return proxies

def urlcrawl(url):
    pagetext = requests.get(url, headers={'User-Agent': ua.msie})  # 可能报错//获取不到页面
    print(pagetext.status_code)
    html = etree.HTML(pagetext.text)
    pageurllist = html.xpath('.//td[@class="tal f14"]/a/@href')
    pageurllist = ['https:'+url for url in pageurllist]
    print(pageurllist)
    return pageurllist

# 单独页
def reachcrawl(stackname,pageurllist,i):
    csv_file = open('data//news_data//' + f'{stackname}研究报告第{i}页.csv', 'w', newline='', encoding='utf-8')
    f = csv.writer(csv_file)
    for url in pageurllist:
        htmltext = requests.get(url, headers={'User-Agent': ua.msie})
        html = etree.HTML(htmltext.text)
        title = html.xpath('//div[@class="content"]/h1/text()')
        category = html.xpath('//div[@class="content"]/div[1]/span[1]/text()')
        institution = html.xpath('//div[@class="content"]/div[1]/span[2]/a/text()')
        researcher = html.xpath('//div[@class="content"]/div[1]/span[3]/a/text()')
        date = html.xpath('//div[@class="content"]/div[1]/span[4]/text()')
        content = html.xpath('//div[@class="content"]/div[2]/p/text()')
        print([title[0], category[0][3:], institution[0], researcher[0], date[0][3:], ''.join(content).strip()])
        f.writerow([title[0], category[0][3:], institution[0], researcher[0], date[0][3:], ''.join(content).strip()])
    csv_file.close()


# 华工科技（SZ.000988）
if __name__ == '__main__':
    stockname = '华工科技'
    url = 'https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?symbol=000988&t1=all&p=7'
    reachcrawl(stockname, urlcrawl(url), url.split('=')[-1])