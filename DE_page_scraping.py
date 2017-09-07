def ams_data(search_text, num, low_price='', high_price=''):
    import requests
    from bs4 import BeautifulSoup
    import time

    def price_get(sku):
        try:
            float(sku.parent.parent.parent.next_sibling.find('span', {'class': 'a-size-base'}).get_text().split()[-1].replace(',', '.'))
        except Exception as err:
            r = 0
        else:
            r = float(sku.parent.parent.parent.next_sibling.find('span', {'class': 'a-size-base'}).get_text().split()[-1].replace(',', '.'))
        return r

    def asin_get(sku):
        try:
            sku.parent.parent.parent.parent.parent.parent.parent.parent.attrs['data-asin']
        except Exception as err:
            r = 0
        else:
            r = sku.parent.parent.parent.parent.parent.parent.parent.parent.attrs['data-asin']
        return r

    def star_get(sku):
        try:
            #float(sku.parent.parent.parent.next_sibling.find('span', {'class': 'a-icon-alt'}).get_text().split()[0].replace(',', '.'))
            float(sku.parent.parent.parent.next_sibling.findAll('span', {'class': 'a-icon-alt'})[-1].get_text().split()[0].replace(',', '.'))
        except Exception as err:
            r = 0
        else:
            #r = float(sku.parent.parent.parent.next_sibling.find('span', {'class': 'a-icon-alt'}).get_text().split()[0].replace(',', '.'))
            r = float(sku.parent.parent.parent.next_sibling.findAll('span', {'class': 'a-icon-alt'})[-1].get_text().split()[0].replace(',', '.'))
        return r

    def review_get(sku):
        try:
            int(sku.parent.parent.parent.next_sibling.findAll('a', {'class': 'a-size-small'})[-1].get_text())
            #int(sku.parent.parent.parent.next_sibling.find('a', {'class': 'a-size-small'}).get_text())
        except Exception as err:
            r = 0
        else:
            r = int(sku.parent.parent.parent.next_sibling.findAll('a', {'class': 'a-size-small'})[-1].get_text())
            #r = int(sku.parent.parent.parent.next_sibling.find('a', {'class': 'a-size-small'}).get_text())
        return r

    def brand_get(sku):
        try:
            sku.parent.parent.next_sibling.findAll('span', {'class': 'a-size-small'})[-1].get_text()
        except Exception as err:
            r = 0
        else:
            r = sku.parent.parent.next_sibling.findAll('span', {'class': 'a-size-small'})[-1].get_text()
        return r

    def title_get(sku):
        try:
            sku.attrs['data-attribute']
        except Exception:
            r = 'unknown'
        else:
            r = sku.attrs['data-attribute']
        return r


    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36'}
    search_text = search_text.replace(' ', '%20')
    url = 'https://www.amazon.de/s/keywords=' + search_text + '&page={}' + '&low-price={}' + '&high-price={}'
    url = url.format(num, low_price, high_price)
    lst = []
    time.sleep(1)
    wb_data = requests.get(url, headers=headers)
    bsObj = BeautifulSoup(wb_data.text, 'lxml')
    skus = bsObj.findAll('h2', {'class': 'a-size-medium'})
    for sku in skus:
        data = {
            'title': title_get(sku),
            'brand': brand_get(sku),
            'price': price_get(sku),
            'asin': asin_get(sku),
            'star': star_get(sku),
            'review': review_get(sku),
            'time': time.strftime('%Y/%m/%d'),
        }
        lst.append(data)
    return lst


def ams_scrape(search_text, num, low_price, high_price):
    from multiprocessing import Pool

    # 填充搜索参数的列表
    info_lst = []
    for num in range(1, num+1):
        info = [search_text, num, low_price, high_price]
        info_lst.append(info)

    # 完成抓取，得到list对象
    pool = Pool()
    temp = []
    lst = []
    for info in info_lst:
        temp.append(pool.apply_async(ams_data, args=(info[0], info[1], info[2], info[3], )))
    pool.close()
    pool.join()

    for item in temp:
        lst.append(item.get())
    return lst
    # 返回dataframe
    # d = {}
    # for i in range(len(lst)):
    #     d[i] = pd.DataFrame(lst[i])
    # df = pd.concat([d[i] for i in range(len(d))])
    # return df
