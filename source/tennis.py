import requests
from bs4 import BeautifulSoup

url = 'https://www.tennisvlaanderen.be/clubdashboard?clubId=2'
url = 'https://www.tennisvlaanderen.be/clubdashboard?clubId=2000'
job_list = []
for p in range(1):
    res = requests.get(url).text
    soup = BeautifulSoup(res, features="html.parser")

    errormsg = soup.findAll('li', attrs={'class': 'portlet-msg-error'})
    print(len(errormsg))

    jobs = soup.findAll('li', attrs={'class': 'clearfix'})
    print(len(jobs))
    for job in jobs:
        print(job.find('span', attrs={'class': 'list-value'}).text)
        '''
        job_list.append(job_summary)
        '''

    courts = soup.findAll('tr', attrs={'class': 'ui-widget-content', 'role': 'row'})
    print(len(courts))
    for co in courts:
        try:
            print(co.find('td', attrs={'data-title': 'Aantal'}).text, end='')
            print(co.find('td', attrs={'data-title': 'Sport'}).text, end='')
            print(co.find('td', attrs={'data-title': 'Ondergrond'}).text, end='')
            print(co.find('td', attrs={'data-title': 'Type'}).text, end='')
            print(co.find('td', attrs={'data-title': 'Verlicht'}).text, end='')
            print(co.find('td', attrs={'data-title': 'Overdekt'}).text, end='')
            # print(co.find('td', attrs={'data-title':'Adres'}).text, end='')
            print()
        except:
            pass