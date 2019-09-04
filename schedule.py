from pprint import pprint as pp
from bs4 import BeautifulSoup
import urllib3
import json

http = urllib3.PoolManager()

with open('ids') as file:
    ids = json.load(file)

routes = []

i = 0

while i < len(ids):
    url = 'https://swrailway.gov.ua/timetable/eltrain/?tid=' + str(ids[i])
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, features="lxml")

    try:
        route = {'route': soup.find('tr', {'class': 'onx'})
                 .find('b').string, 'stations': []}

        for st in soup.findAll('tr', {'class': ['onx', 'on']})[2:]:
            try:
                time = [st.findAll('td', {'class': ['q0', 'q1']})[1].string,
                        st.findAll('td', {'class': ['q0', 'q1']})[2].string,
                        st.findAll('td', {'class': ['q0', 'q1']})[3].string]

                route['stations'].append({'name': (str(
                    st.find('a', {'class': 'et'}).string)[4:-4]
                    if st.find('b') is None
                    else st.find('b').string),
                    'arrival': time[0],
                    'departure': time[1],
                    'stop': time[2]})

            except AttributeError:
                pass

        routes.append(route)

    except AttributeError:
        print('Blocked!')
        i -= 1
        input()

    i += 1

pp(routes)
