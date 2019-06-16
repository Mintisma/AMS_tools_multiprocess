import time
import re
import requests
from scrapy.selector import Selector
s = requests.session()


def ams_data(search_text, num, low_price, high_price):
    def star_get(sku):
        try:
            r = float((sku.xpath('div/span[1]/@aria-label').extract_first('').split()[0]))
        except Exception as err:
            r = 0
        return r

    def review_get(sku):
        try:
            r = int(sku.xpath('div/span[2]/@aria-label').extract_first('').replace(',', ''))
        except Exception as err:
            r = 0
        return r

    def price_get(sku):
        try:
            r = float(sku.xpath('div/div/div/div/div/a/span/span[1]/span/text()').extract_first('').replace('$', ''))
        except Exception as err:
            r = 0
        return r

    def asin_get(sku):
        href = sku.xpath('a/@href').extract_first()
        try:
            match_r = re.match('.+/dp/(\w+)/ref.+', href)
            r = match_r.group(1)
        except Exception as e:
            r = 'ads'
        return r

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36'}
    search_text = search_text.replace(' ', '%20')
    url = 'https://www.amazon.de/s?k=' + search_text + '&page={}'
    url = url.format(num, low_price, high_price)
    lst = []
    time.sleep(1)
    r = s.get(url, headers=headers)
    selector = Selector(text=r.text)
    skus = selector.xpath('//h2[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-2"]')
    for sku in skus:
        title = sku.xpath('a/span/text()').extract_first('')
        data = {
            'time': time.strftime('%Y/%m/%d'),
            'title': title,
            'brand': title.split()[0],
            'asin': asin_get(sku),
        }
        sku = sku.xpath('parent::div/following-sibling::div')
        data['star'] = star_get(sku)
        data['review'] = review_get(sku)

        sku = sku.xpath('parent::div/parent::div/parent::div/following-sibling::div')
        data['price'] = price_get(sku)
        if low_price <= data['price'] <= high_price:
            lst.append(data)
    #     df = pd.DataFrame(lst)
    #     df.drop_duplicates('asin', inplace=True)
    #     df = df[(df.price >= low) & (df.price <= high)]
    return lst


def ams_scrape(search_text, num, low_price, high_price):
    from multiprocessing import Pool

    # 填充搜索参数的列表
    info_lst = []
    for num in range(1, num+1):
        info = [search_text, num, low_price, high_price]
        info_lst.append(info)

    # 完成抓取，得到list对象
    pool = Pool(4)
    temp = []
    lst = []
    for info in info_lst:
        temp.append(pool.apply_async(ams_data, args=(info[0], info[1], info[2], info[3], )))
    pool.close()
    pool.join()

    for item in temp:
        lst.append(item.get())
    return lst

    # # 返回dataframe
    # d = {}
    # for i in range(len(lst)):
    #     d[i] = pd.DataFrame(lst[i])
    # df = pd.concat([d[i] for i in range(len(d))])
    # return df
