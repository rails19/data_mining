from bs4 import BeautifulSoup
import urllib3
from pprint import pprint as pp


def getPrices():
    """
        Returns a list of price tables.
        Every table is a dict consisting of 'name' and 'lines'.

        'name' - string with table № and some info.
        'lines' - list of table lines
    """

    # CRAWLING THE WEBPAGE

    http = urllib3.PoolManager()

    response = http.request(
        'GET', 'https://swrailway.gov.ua/timetable/eltrain/attention/')
    soup = BeautifulSoup(response.data, features="lxml")

    # GETTING NAMES AND DATA OF ALL TABLES

    divs = [div for div in soup.findAll(
        'td', {'colspan': '2'})[6].findAll('div')]
    tables = soup.findAll('td', {'colspan': '2'})[6].findAll('table')

    # MERGING ALL THE DATA INTO ONE LIST

    prices = {}
    regions = ['KYIV', 'ZSVH', 'CHER']
    region_ptr = -1

    for i in range(len(tables)):

        name = str(divs[i])[52:-6].split('<br/>')

        if len(name) == 3:

            prices[regions[region_ptr]].append({})

            (prices[regions[region_ptr]]
                   [len(prices[regions[region_ptr]]) - 1]
                   ['name']) = (name[0] + '\n' +
                                name[1] + '\n' +
                                name[2])

            (prices[regions[region_ptr]]
                   [len(prices[regions[region_ptr]]) - 1]
                   ['lines']) = []

            for tr in tables[i].findAll('tr'):
                (prices[regions[region_ptr]]
                       [len(prices[regions[region_ptr]]) - 1]
                       ['lines'].append([td.text for td in tr.findAll('td')]))
        else:
            region_ptr += 1
            prices[regions[region_ptr]] = []

    return prices


pp(getPrices())
