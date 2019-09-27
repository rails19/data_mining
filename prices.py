from bs4 import BeautifulSoup
import urllib3


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

    prices = []

    # MERGING ALL THE DATA INTO ONE LIST

    for i in range(len(tables)):
        prices.append({})
        prices[i]['name'] = (str(divs[i])[52:-6].split('<br/>')[0] + '\n' +
                             str(divs[i])[52:-6].split('<br/>')[1] + ' ' +
                             str(divs[i])[52:-6].split('<br/>')[2])

        prices[i]['lines'] = []

        for r in tables[i].findAll('tr'):
            prices[i]['lines'].append([d.text for d in r.findAll('td')])

    return prices
