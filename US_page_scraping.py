def ams_data(search_text, num, low_price='', high_price=''):
    import requests
    from bs4 import BeautifulSoup
    import time

    def star_get(sku):
        try:
            float(sku.parent.parent.parent.next_sibling.findAll('span', {'class': 'a-icon-alt'})[-1].get_text().split()[
                      0])
        except Exception as err:
            r = 0
        else:
            r = float(
                sku.parent.parent.parent.next_sibling.findAll('span', {'class': 'a-icon-alt'})[-1].get_text().split()[
                    0])
        return r

    def review_get(sku):
        try:
            int(sku.parent.parent.parent.next_sibling.find('a', {'class': 'a-size-small'}).get_text())
        except Exception as err:
            r = 0
        else:
            r = int(sku.parent.parent.parent.next_sibling.find('a', {'class': 'a-size-small'}).get_text())
        return r

    def price_get(sku):
        try:
            int(sku.parent.parent.parent.next_sibling.find('span', {'class': 'sx-price-whole'}).get_text().replace(',',
                                                                                                                   '')) + float(
                sku.parent.parent.parent.next_sibling.find('sup', {'class': 'sx-price-fractional'}).get_text()) / 100
        except Exception as err:
            r = 0
        else:
            r = int(
                sku.parent.parent.parent.next_sibling.find('span', {'class': 'sx-price-whole'}).get_text().replace(',',
                                                                                                                   '')) + float(
                sku.parent.parent.parent.next_sibling.find('sup', {'class': 'sx-price-fractional'}).get_text()) / 100
        return r

    def asin_get(sku):
        try:
            sku.parent.parent.parent.parent.parent.parent.parent.parent.attrs['data-asin']
        except Exception as err:
            r = 0
        else:
            r = sku.parent.parent.parent.parent.parent.parent.parent.parent.attrs['data-asin']
        return r

    def brand_get(sku):
        try:
            sku.parent.parent.next_sibling.findAll('span', {'class': 'a-size-small'})[-1].get_text()
        except Exception:
            r = 'unknown'
        else:
            r = sku.parent.parent.next_sibling.findAll('span', {'class': 'a-size-small'})[-1].get_text()
        return r

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36'}
    search_text = search_text.replace(' ', '%20')
    url = 'https://www.amazon.com/s/keywords=' + search_text + '&page={}' + '&low-price={}' + '&high-price={}'
    url = url.format(num, low_price, high_price)
    lst = []
    time.sleep(1)
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    skus = soup.findAll('h2', {'class': 'a-size-medium'})
    for sku in skus:
        data = {
            'time': time.strftime('%Y/%m/%d'),
            'title': sku.get('data-attribute'),
            'star': star_get(sku),
            'review': review_get(sku),
            'asin': asin_get(sku),
            'price': price_get(sku),
            'brand': brand_get(sku)
        }
        lst.append(data)
    # df = pd.DataFrame(lst)
    #df.drop_duplicates('asin', inplace=True)
    #df = df[(~df['title'].str.contains('Inateck')) & (~df['title'].str.contains('Tomons')) & (~df['title'].str.contains('Tomtoc'))]
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
