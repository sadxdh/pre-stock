# 数据采集-研究报告-爬虫部分

# 数据采集  新浪财经  股票对应研究报告
# data_collection/news_collection/getStockResearchReport.py
# 示例网址：https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?symbol=002415&t1=all&p=1
# url两个重要参数：
#   symbol：股票代码
#   p：研究报告页码
# 网站反爬机制
# 同一ip频繁访问会有五分钟的拒绝访问，具体表现为：页面重定向
#   添加headers应对反扒效果并不明显
#   解决方案：使用代理池（在开源项目基础上进行改写）
#     源项目：https://github.com/Python3WebSpider/ProxyPool.git
#     代理池原理：三大部分：获取模块、存储模块、检查模块
#        获取模块：https://cuiqingcai.com/7048.html
#        存储模块：https://cuiqingcai.com/7048.html
#        检查模块：https://cuiqingcai.com/7048.html

# 使用requests，Redis数据库，etree，xpath，CSV
# 设置全局变量为headers，使用fake_useragent伪造UA

# 爬虫脚本
# getStockResearchReport.py
# getproxy:
#   连接到本地Redis数据库
#      redis中使用key获取value，从所有的value中提取得分最高的代理
#   获取所有键名为"use_proxy"的键的值
#   从值中筛选出"last_status": true的键
#   从筛选后的键中随机选择一个键

# getNumPage(code):
# https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?symbol=002415&t1=all
# 使用requests访问研究报告首页，获取研究报告页数长度

# reports:
# 单独页面的研究报告爬虫，用于爬取页面内所有研究报告对应页面的报告详情，然后保存到CSV文件中
# 每一个单独页面的所有研究报告保存在一个CSV表格中
# 在循环请求与分析单独研究报告之前创建CSV对象，请求的同时对CSV文件进行写入，在每一页全部爬取完成时释放变量
# title（标题）, category（机构类型）, institution（公司名称）, researcher（研究员）, date（日期）, content（内容）
# 为了提高代码的健壮性，其中添加了异常捕获结构，用于判断页面内容与字段内容是否正常获取

# main（主程序）:
# 读取target文件中的目标股票名称和股票对应代码
# 使用循环调用方法实现自动爬取
# 设置时间间隔，一定程度上减少网页访问拒绝

#
# 改进：可以添加多线程模块，加快爬取速度
# 指定研究报告下载.py
# 可实现自动爬取，生成xxxx研究报告第x页.csv'
# 注：该脚本读取和写入的文件夹都为：data/news_data
# 在getStockResearchReport.py的基础上改写，实现对某一特定研究报告的爬取，防止循环爬取脚本部分信息获取不全问题

import requests
from lxml import etree
import csv
import time
import fake_useragent
import redis
import json
import random
from requests.exceptions import ProxyError
ua = fake_useragent.UserAgent()


# 代理池
def getproxy():
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


def getNumPage(code):
    # https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?symbol=002415&t1=all
    url = f"https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?symbol={code}&t1=all"
    resp = requests.get(url, headers={'User-Agent': ua.firefox}, proxies=getproxy())
    # print(resp.text)
    # page_count = 1
    page_count = etree.HTML(resp.text).xpath('//*[@id="_function_code_page"]/span[10]/a/@onclick')[0].split("'")[1]
    print(f"研究报告共{page_count}页")
    return page_count


# 被识别为爬虫会限制五分钟内拒绝访问
def reports(stock, code, page):
    global resp, htmlpage
    print(f"{stock}研究报告第{page}页")
    # https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?symbol=600000&t1=all&p=8
    url = f"https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?symbol={code}&t1=all&p={page}"
    print(url)
    while True:
        try:
            resp = requests.get(url, headers={'User-Agent': ua.firefox}, proxies=getproxy(), verify=False)
        except ProxyError:
            print(f'{ProxyError},IP失效，标题页面内容无法获取，正在更换IP。。。。')
        else:
            # print(resp.text)
            page_html = etree.HTML(resp.text)
            trs = ['https:' + i for i in page_html.xpath('//td[@class="tal f14"]/a/@href')]
            print(trs)
            csv_file = open('data//news_data//' + f'{stock}研究报告第{page}页.csv', 'w', newline='', encoding='utf-8')
            f = csv.writer(csv_file)
            for tr in trs:
                time.sleep(2)
                while True:
                    try:
                        htmlpage = requests.get(tr, headers={'User-Agent': ua.firefox}, proxies=getproxy(),
                                                verify=False)
                    except ProxyError:
                        print(f'{ProxyError},IP失效，研究报告页面内容无法获取，正在更换IP。。。。')
                    else:
                        # print(htmlpage.text)
                        html = etree.HTML(htmlpage.text)
                        title = html.xpath('//div[@class="content"]/h1/text()')
                        category = html.xpath('//div[@class="content"]/div[1]/span[1]/text()')
                        institution = html.xpath('//div[@class="content"]/div[1]/span[2]/a/text()')
                        researcher = html.xpath('//div[@class="content"]/div[1]/span[3]/a/text()')
                        date = html.xpath('//div[@class="content"]/div[1]/span[4]/text()')
                        content = html.xpath('//div[@class="content"]/div[2]/p/text()')
                        print([title[0], category[0][3:], institution[0], researcher[0], date[0][3:],
                               ''.join(content).strip()])
                        f.writerow([title[0], category[0][3:], institution[0], researcher[0], date[0][3:],
                                    ''.join(content).strip()])
            csv_file.close()


def main():
    f = open('target', 'r', encoding='utf-8')
    stock_name = f.read().split('\n')
    print(stock_name)
    for s in stock_name:
        stock = s.split('（')[0]
        code = s.split('.')[-1].split('）')[0]
        print(stock)
        print(code)
        # 启动爬虫获取获取页数、页面响应
        page_count = getNumPage(code)
        print(page_count)
        # # 爬取内容
        for i in range(1, int(page_count)+1):
            reports(stock, code, i)
        time.sleep(2)


if __name__ == '__main__':
    main()

