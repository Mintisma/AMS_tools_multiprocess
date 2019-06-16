import requests
from bs4 import BeautifulSoup
import time
import re
from scrapy.selector import Selector

s = requests.session()


def get_top100(index, num):
    def price_get(sku):
        try:
            r = float(sku.xpath('span/div/span/div[2]/a/span/span/text()').extract_first('').replace('$', ''))
        except Exception as err:
            r = 0
        return r

    def star_get(sku):
        try:
            r = float(sku.xpath('span/div/span/div[1]/a[1]/@title').extract_first('').split()[0])
        except Exception as err:
            r = 0
        return r

    def review_get(sku):
        try:
            r = int(sku.xpath('span/div/span/div[1]/a[2]/text()').extract_first('').replace(',', ''))
        except Exception as err:
            r = 0
        return r

    def asin_get(sku):
        try:
            title = sku.xpath('span/div/span/div[2]/a/@href').extract_first('')
            match_r = re.match('.+/dp/(\w+)/ref.+', title)
            r = match_r.group(1)
        except Exception as err:
            r = 'unknown'
        return r

    def brand_get(title):
        try:
            r = title.split()[0]
        except Exception as err:
            r = 'unknown'
        return r

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36'}
    url = 'https://www.amazon.com/gp/bestsellers/hi/{}?pg={}'.format(index, num)

    lst = []
    time.sleep(1)
    r = s.get(url, headers=headers)
    selector = Selector(text=r.text)
    skus = selector.xpath('//ol[@id="zg-ordered-list"]/li[@class="zg-item-immersion"]')
    for sku in skus:
        title = sku.xpath('span/div/span/a/div/text()').extract_first('').strip()
        data = {
            'time': time.strftime('%Y/%m/%d/%H'),
            'rank': int(sku.xpath('span/div/div/span/span/text()').extract_first('').replace('#', "")),
            'brand': brand_get(title),
            'star': star_get(sku),
            'review': review_get(sku),
            'price': price_get(sku),
            'title': title,
            'asin': asin_get(sku),
        }
        lst.append(data)
    return lst


def ams_scrape(index):
    from multiprocessing import Pool

    # 填充搜索参数的列表
    info_lst = []
    for num in range(1, 3):
        info = [index, num]
        info_lst.append(info)

    # 完成抓取，得到list对象
    pool = Pool(4)
    temp = []
    lst = []
    for info in info_lst:
        temp.append(pool.apply_async(get_top100, args=(info[0], info[1])))
    pool.close()
    pool.join()

    for item in temp:
        lst.append(item.get())
    return lst
