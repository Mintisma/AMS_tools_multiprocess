def get_top100(index, num):
    import requests
    from bs4 import BeautifulSoup
    import time

    def price_get(sku):
        try:
            int(sku.parent.find('span', {'class': 'a-size-base'}).get_text().replace('￥', '').replace(',', ''))
        except Exception as err:
            r = 0
        else:
            r = int(sku.parent.find('span', {'class': 'a-size-base'}).get_text().replace('￥', '').replace(',', ''))
        return r

    def star_get(sku):
        try:
            float(sku.parent.find('span', {'class': 'a-icon-alt'}).get_text().split()[1])
        except Exception as err:
            r = 0
        else:
            r = float(sku.parent.find('span', {'class': 'a-icon-alt'}).get_text().split()[1])
        return r

    def review_get(sku):
        try:
            sku.parent.find('a', {'class': 'a-size-small'}).get_text()
        except Exception as err:
            r = 0
        else:
            r = int(sku.parent.find('a', {'class': 'a-size-small'}).get_text().replace(',', ''))
        return r

    def asin_get(sku):
        try:
            sku.parent.find('a', {'class': 'a-size-small'}).get('href').split('/')[2]
        except Exception as err:
            r = 'unknown'
        else:
            r = sku.parent.find('a', {'class': 'a-size-small'}).get('href').split('/')[2]
        return r

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36'}
    url = 'https://www.amazon.co.jp/gp/bestsellers/computers/{}?pg={}'.format(index, num)

    lst = []
    time.sleep(1)
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    skus = soup.select('div.zg_rankLine')
    for sku in skus:
        data = {
            'time': time.strftime('%Y/%m/%d/%H'),
            'rank': int(sku.find('span', {'class': 'zg_rankNumber'}).get_text().strip().replace('.', '')),
            'brand': sku.parent.find('div', {'class': 'p13n-sc-truncate'}).get_text().strip().split()[0],
            'star': star_get(sku),
            'review': review_get(sku),
            'price': price_get(sku),
            'title': sku.parent.find('div', {'class': 'p13n-sc-truncate'}).get_text().strip(),
            'asin': asin_get(sku),
        }
        lst.append(data)
    return lst


def ams_scrape(index):
    from multiprocessing import Pool

    # 填充搜索参数的列表
    info_lst = []
    for num in range(1, 6):
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
