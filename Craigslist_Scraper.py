import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

def find_size_and_brs(apt_size):
    x = apt_size.split( "\n" )
    x[1] = x[1].rstrip(' -')
    x[2] = x[2].rstrip(' -')

    if len(x) == 4:
        n_brs = x[1].replace('br', '')
        this_size = x[2].replace('ft', '')
    elif 'br' in x[1]:
        # It's the n_bedrooms
        n_brs = x[1].replace('br', '')
        this_size = np.nan
    elif 'ft' in x[1]:
        # It's the size
        this_size = x[1].replace('ft', '')
        n_brs = np.nan
    return float(this_size), float(n_brs)

def find_times(results):
    times = []
    for rw in apts:
        if time is not None:
            time = time['datetime']
            time = pd.to_datetime(time)
        else:
            time = np.nan
        times.append(time)
    return times

loc_prefixes = ['eby', 'nby', 'sfc', 'sby', 'scz']
ok = ['apa','sub','roo']

results = []

search_indices = np.arange(0, 300, 120)

for loc in loc_prefixes[0]:
    for i in search_indices:
        url = 'http://sfbay.craigslist.org/search/{0}/apa'.format(loc)
        resp = requests.get(url, params={'bedrooms': 1, 's': i})

        txt = BeautifulSoup(resp.text, 'html.parser')

        apts = txt.findAll('li', attrs={'class': 'result-row'})

        links = []
        sizes_brs = []
        title = []
        time = []
        prices = []

        for this_apt in apts:
            apt_link = this_apt.find('a', attrs={'class': 'result-title hdrlnk'})['href']
            lst = apt_link.split('/')

            if lst[4] not in ok:
                continue
            else:
                #create list of links
                links.append(apt_link)

                #create list of rooms sizes and # of bedrooms
                apt_size = this_apt.findAll(attrs={'class': 'housing'})[0].text
                sizes_brs.append(find_size_and_brs(apt_size))

                #create list of titles
                apt_title = this_apt.find('a', attrs={'class': 'result-title hdrlnk'}).text
                title.append(apt_title)

                #create list of times posted
                apt_time = pd.to_datetime(this_apt.find('time')['datetime'])
                time.append(apt_time)

                #Create a list of apt prices
                price = this_apt.find('span', {'class': 'result-price'})
                if price is not None:
                    price = float(price.text.strip('$'))
                else:
                    price = np.nan
                prices.append(price)

        #Creates SEPARATE list of room sizes and # of bedrooms
        sizes, n_brs = zip(*sizes_brs)

        data = np.array([time, prices, sizes, n_brs, title, links])
        col_names = ['time', 'price', 'size', 'brs', 'title', 'link']
        df = pd.DataFrame(data.T, columns=col_names)
        df = df.set_index('time')

        # Add the location variable to all entries
        df['loc'] = loc
        results.append(df)

# Finally, concatenate all the results
results = pd.concat(results, axis=0)
#print(results)

results.to_csv('craigslist_results.csv')
