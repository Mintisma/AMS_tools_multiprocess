from spyre import server
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import UK_page_scraping
import DE_page_scraping
import JP_page_scraping
import US_page_scraping
import US_top100, UK_top100, DE_top100, JP_top100


class AmsInteract(server.App):
    title = 'Search For Asins'

    countries = [
        {'label': 'US', 'value': 'US'},
        {'label': 'UK', 'value': 'UK'},
        {'label': 'DE', 'value': 'DE'},
        {'label': 'JP', 'value': 'JP'}
    ]
    inputs = [
            {
                'type': 'dropdown',
                'label': 'Country',
                'options': countries,
                'key': 'country',
                'action_id': 'update_search',
        },
            {
                'type': 'text',
                'label': 'top100_index',
                'key': 'top100_index',
                'action_id': 'update_search',
        },
            {
                'type': 'text',
                'key': 'search',
                'label': 'search term',
                'action_id': 'update_search'
        },
            {
                'type': 'slider',
                'label': 'number of pages',
                "min": 2, "max": 10, "value": 2,
                'key': 'page',
                'action_id': 'update_search'
        },
            {
                'type': 'text',
                'label': 'title_contains',
                'key': 'title_contains',
                'action_id': 'update_search'
        },
            {
                'type': 'text',
                'label': 'title_notContains',
                'key': 'title_notContains',
                'action_id': 'update_search'
        },
            {
                'type': 'text',
                'label': 'brand',
                'key': 'brand',
                'action_id': 'update_search'
        },
            {
                'type': 'slider',
                'label': 'minimum price',
                'key': 'price_min',
                'action_id': 'update_search',
                "min": 0, "max": 4000, "value": 0
        },
            {
                'type': 'slider',
                'label': 'max price',
                'key': 'price_max',
                'action_id': 'update_search',
                "min": 1, "max": 200000, "value": 10
        }
    ]

    controls = [
        {
            'type': 'button',
            'label': 'Search',
            'id': 'update_search'
    }
    ]

    tabs = ['Plot', 'Table', 'ASINS']

    outputs = [
        {
            'type': 'plot',
            'id': 'plot',
            'control_id': 'update_search',
            'tab': 'Plot'
    },
        {
            'type': 'table',
            'id': 'table',
            'control_id': 'update_search',
            'tab': 'Table'
    },
        {
            'type': 'html',
            'id': 'html',
            'tab': 'ASINS',
            'control_id': 'update_search',
    }
    ]

    def getData(self, params):
        top100_index = params['top100_index']
        search = params['search']
        page = int(params['page'])
        country = params['country']
        title_contains = list(str(params['title_contains']).split(','))
        title_notContains = list(str(params['title_notContains']).split(','))
        brand = str(params['brand'])
        price_max = int(params['price_max'])
        price_min = int(params['price_min'])

        # country & search
        if top100_index == '' and search != '':
            if country == 'UK':
                lst = UK_page_scraping.ams_scrape(search, page, price_min, price_max)
            elif country == 'US':
                lst = US_page_scraping.ams_scrape(search, page, price_min, price_max)
            elif country == 'DE':
                lst = DE_page_scraping.ams_scrape(search, page, price_min, price_max)
            elif country == 'JP':
                lst = JP_page_scraping.ams_scrape(search, page, price_min, price_max)
        elif top100_index != '':
            if country == 'US':
                lst = US_top100.ams_scrape(top100_index)
            elif country == 'UK':
                lst = UK_top100.ams_scrape(top100_index)
            elif country == 'DE':
                lst = DE_top100.ams_scrape(top100_index)
            elif country == 'JP':
                lst = JP_top100.ams_scrape(top100_index)

        # transform list to DataFrame
        if len(lst) > 0:
            #df = pd.DataFrame(lst)
            d = {}
            for i in range(len(lst)):
                d[i] = pd.DataFrame(lst[i])
            df = pd.concat([d[i] for i in range(len(d))])

            df.drop_duplicates('asin', inplace=True)
            df = df[df.asin!='unknown']
            df = df[(~df.title.str.contains('Inateck')) & (~df.title.str.contains('Tomons')) & (~df.title.str.contains('Tomtoc'))]

            # contains
            if title_contains[0] != '':
                for title_contain in title_contains:
                    df = df[(df.title.str.contains(title_contain))]
            if title_notContains[0] != '':
                for title_notContain in title_notContains:
                    df = df[(~df.title.str.contains(title_notContain))]
            if brand != '':
                df = df[df.brand.str.contains(brand)]
            # # price
            df = df[(df.price>=price_min) & (df.price<=price_max)]
            return df

    def getPlot(self, params):
        df = self.getData(params)
        fig = plt.figure()  # make figure object
        splt = fig.add_subplot(1, 1, 1)
        splt.set_xlabel('price')
        splt.set_ylabel('number')
        splt.hist(df.price, bins=10)
        return splt

    def getHTML(self, params):
        df = self.getData(params)
        Asins = '|'.join(list(df.asin))
        info = '<b>The Asins we want are: <b> <br><br> {} <br><br> \
            The total Asins number are: <br> {}'.format(Asins, df.shape[0])
        return info

app = AmsInteract()
app.launch(host='0.0.0.0',port=8001)