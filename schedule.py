"""
    Writes routes with all additional info to database
"""

from pprint import pprint as pp
from bs4 import BeautifulSoup
import urllib3
import json

http = urllib3.PoolManager()

with open('ids') as file:
    ids = json.load(file)

routes = []

i = 0

# CRAWLING ALL OF THE ROUTES

while i < len(ids):
    url = 'https://swrailway.gov.ua/timetable/eltrain/?tid=' + str(ids[i])
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, features="lxml")

    try:

        # CREATING A ROUTE DICT

        route_name = soup.find('tr', {'class': 'onx'}).find('b').string
        route_train = soup.find('tr', {'class': 'onx'}).find(
            'td', {'colspan': '3'}).find('b').string

        route = {'id': ids[i],
                 'name': route_name,
                 'train': route_train,
                 'stations': []}

        for st in soup.findAll('tr', {'class': ['onx', 'on']})[2:]:

            # CREATING A STATION DICT

            try:

                # TODO: cast to right time format

                time = [st.findAll('td', {'class': ['q0', 'q1']})[1]
                        .string.split(':'),
                        st.findAll('td', {'class': ['q0', 'q1']})[2]
                        .string.split(':')]

                # TODO: maybe links will be changed in the future

                station_id = st.find('a', {'class': 'et'})['href'][-9:-5]

                station_name = (st.find('a', {'class': 'et'}).string[9:-4]
                                if st.find('b') is None
                                else st.find('b').string)

                station_isPlatform = False if st.find('b') else True

                route['stations'].append({
                    'id': station_id,
                    'name': station_name,
                    'isPlatform': station_isPlatform,
                    'arrival': time[0],
                    'departure': time[1]})

            except AttributeError:
                pass

        routes.append(route)

    except AttributeError:
        print('Blocked!')
        i -= 1
        input()

    i += 1

# TODO: Write to database

pp(routes)

with open('rts', 'w') as outfile:
    json.dump(routes, outfile)
