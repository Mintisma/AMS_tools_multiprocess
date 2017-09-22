def ams_data(search_text, num, low_price='', high_price=''):
    import requests
    from bs4 import BeautifulSoup
    import time

    def star_get(sku):
        try:
            float(sku.parent.parent.parent.next_sibling.next_sibling.find('span', {'class': 'a-icon-alt'}).get_text().split()[-1])
        except Exception as err:
            r = 0
        else:
            r = float(sku.parent.parent.parent.next_sibling.next_sibling.find('span', {'class': 'a-icon-alt'}).get_text().split()[-1])
        return r


    def price_get(sku):
        try:
            int(sku.parent.parent.parent.next_sibling.find('span', {'class': 'a-size-base'}).get_text().replace('￥', '').replace(',', '').strip().split()[0])
        except Exception as err:
            r = 0
        else:
            r = int(sku.parent.parent.parent.next_sibling.find('span', {'class': 'a-size-base'}).get_text().replace('￥', '').replace(',', '').strip().split()[0])
        return r

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36'}
    search_text = search_text.replace(' ', '%20')
    url = 'https://www.amazon.co.jp/s/keywords=' + search_text + '&page={}' + '&low-price={}' + '&high-price={}'
    url = url.format(num, low_price, high_price)

    lst = []
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    skus = soup.findAll('h2', {'class': 's-inline'})
    for sku in skus:
        data = {
            'time': time.strftime('%Y/%m/%d'),
            'title': sku.attrs['data-attribute'],
            'brand': sku.parent.parent.next_sibling.findAll('span', {'class': 'a-size-small'})[-1].get_text(),
            'asin': sku.parent.parent.parent.parent.parent.attrs['data-asin'],
            'price': price_get(sku),
            'star': star_get(sku),
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
    # 返回dataframe
    # d = {}
    # for i in range(len(lst)):
    #     d[i] = pd.DataFrame(lst[i])
    # df = pd.concat([d[i] for i in range(len(d))])
    # return df
