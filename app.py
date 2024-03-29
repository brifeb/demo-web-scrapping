import math
import os
import json
import platform
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")


def millify(n):
    millnames = ['', ' k', ' m', ' b', ' t']
    n = float(n)
    millidx = max(0, min(len(millnames) - 1,
                         int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))

    return '{:.2f}{}'.format(n / 10 ** (3 * millidx), millnames[millidx])


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/steam')
def steam_parser():
    url = 'https://store.steampowered.com/games#p=0&tab=TopSellers'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.182 Safari/537.36 '
    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    titles = soup.find_all('a', attrs={'class': 'tab_item'})

    return render_template('steam-scrapper.html', steam_titles=titles)


@app.route('/detik-populer')
def detik_populer():
    html_doc = requests.get('https://www.detik.com/terpopuler')
    soup = BeautifulSoup(html_doc.text, features='html.parser')
    populer_area = soup.find(attrs={'class': 'grid-row list-content'})
    gambars = populer_area.findAll(attrs={'class': 'media__image'})

    return render_template('detik-scrapper.html', gambars=gambars)


@app.route('/usd-rates')
def idr_rates():
    source = requests.get('http://www.floatrates.com/daily/usd.json')
    json_data = source.json()
    return render_template('rates-scrapper.html', datas=json_data.values())


@app.route('/instagram')
def instagram():
    headers = {
        'cookie': 'mid=W2b0DAAEAAFbGydJZW58lOkhgeoZ; ig_did=80108C7D-D4E0-4DCE-98D3-B74C5A991B81; fbm_124024574287414=base_domain=.instagram.com; ig_nrcb=1; ds_user_id=11167978215; csrftoken=H0wnh0uPuP6R4zUrW727nq8ac253Zj29; sessionid=11167978215:4RS02ZBaFnXSDz:26; shbid=155; datr=LQpLYM8y2nj_4CfS9KDhl9dT; shbts=1617092161.156662; rur=PRN; fbsr_124024574287414=L9IdKKnHtyyHpZJNcidmS5z4CTjMUxjVsDPBbhvfsAg.eyJ1c2VyX2lkIjoiMTI0OTgzMzI4MiIsImNvZGUiOiJBUURNeS0wSXFGUFVYQ0ZaLVpSUFdrcDY3czlZZk1MdXUtWW5hVzJfMjEwYWdMdGNlekxfVG54X2FtS2xSQUQ1SGtvZUwzS0NNWlR1MWctLVJPLWotZGE0OEpYbnYxc18wWG1JaTJ3UWxFcW81Ql9oWjRrN0FtYkZXeS0tZ1JQSUlmYkc0Yl8wOUdoNHhNbXJteFJuQ0lLNFhtX0YtbW5tUDNabTBvTVJkcFdVWXhMRnc3dEdBYldPV1Q2OURBWV9hQ3ZEWVE3d3hHQ3FMQ0syck1LdWowR2dlS3QwY2hvVnFkMXhQREFhTHJLenhfUlZCUDVTQ2xJWHkzckZPM3NpYldGWlVmU3NpbmlDUU4ta3R1R3J2a0RndTRiRHZoeWVtSndUaEttcWkwYnI4bzlnVVZkQnZBcTNtYU91NTN3X0xLNCIsIm9hdXRoX3Rva2VuIjoiRUFBQnd6TGl4bmpZQkFCR2UzanpGZWxXaWE1Q2paQ2tjZTdKbkpmWkExQ1BhZFdHb3Q5Q3Y0VmRyUjNTeEtvQUl1WkM2eEo1V0RuZEVZSW9Ld1I5Z2lMRGVXQ3pkSDhYeGo1NkFmTVRja0daQ1lqVHBiTEFZTWRCSzdsM1R4M0lBclBQVzdhS2VwbFQyelpCc0pxZWZNYkZnVTVvZkFOaTJoUzJsUElQam9xa1pCbE42Y1lDYWJQczVleTlqam9OSndaRCIsImFsZ29yaXRobSI6IkhNQUMtU0hBMjU2IiwiaXNzdWVkX2F0IjoxNjE3MDkyMTY2fQ',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.90 Safari/537.36 '
    }
    ig_users = ['brifeb', 'valeyellow46', 'leomessi', 'gianluigibuffon', 'cristiano', 'marcmarquez93']
    users = []
    for usr in ig_users:
        url = f'https://www.instagram.com/{usr}/?__a=1'
        respon = requests.get(url, headers=headers)
        # print(url, respon)
        res = respon.json()
        # print(res)
        users.append(res['graphql']['user'])
    return render_template('ig-scrapper.html', datas=users)


@app.route('/igtopnine')
def igtopnine():
    # update_img = request.args.get('update') or False
    username = 'valeyellow46'

    with(open(f'{DATA_DIR}/{username}.json', 'r')) as fl:
        profile = json.load(fl)
    with(open(f'{DATA_DIR}/{username}-top9comments.json', 'r')) as fl:
        top_9_comm = json.load(fl)
    with(open(f'{DATA_DIR}/{username}-top9likes.json', 'r')) as fl:
        top_9_likes = json.load(fl)

    top9like_img = []
    top9comm_img = []
    for i in range(9):
        top9like_img.append(f'/static/img/{username}/{username}-{i + 1}-top9likes.jpg')
        top9comm_img.append(f'/static/img/{username}/{username}-{i + 1}-top9comments.jpg')

    # print(top9comm_img)

    return render_template('ig-topnine.html',
                           profile=profile,
                           toplikes=zip(top_9_likes, top9like_img),
                           topcomments=zip(top_9_comm, top9comm_img),
                           millify=millify)


@app.route('/twitter')
def twitter():
    username = 'ladbible'
    size_thumb = 3

    with(open(f'{DATA_DIR}/{username}-vid.json', 'r')) as fl:
        datas = json.load(fl)

    datas = datas[:12]

    return render_template('twitter-scrapper.html', datas=datas, size_thumb=size_thumb, username=username)


@app.route('/linkedin')
def linkerin():
    url = 'https://www.linkedin.com/jobs/engineering-jobs-jakarta'
    job_list = []
    for p in range(1):
        params = {
            'trk': 'homepage-basic_suggested-search',
            'position': 1,
            'pageNum': p
        }
        res = requests.get(url, params=params).text
        soup = BeautifulSoup(res, features="html.parser")
        jobs = soup.findAll('div', attrs={'class': 'job-search-card'})
        print(jobs)
        for job in jobs:
            title = job.find('h3').text
            job_url = job.find('a')['href']
            company = job.find('h4').text
            location = job.find('span', attrs={'class': 'job-search-card__location'}).text
            desc = job.find('p').text
            time = job.find('time').text
            job_summary = {'title': title, 'company': company, 'location': location, 'desc': desc, 'time': time,
                           'job_url': job_url}
            job_list.append(job_summary)

    return render_template('linkedin-scrapper.html', jobs=job_list)


@app.route('/stockbeep')
def stockbeep():
    url = 'https://stockbeep.com/52-week-high-stock-screener'
    url = 'https://stockbeep.com/table-data/52-week-high-stock-screener?hash=c344c83bf4c9b276b59ce5d6dc2c8f0d&country=us&time-zone=-420&sort-column=position&sort-order=desc&_=1617144003884'
    job_list = []
    for p in range(1):
        params = {
            'trk': 'homepage-basic_suggested-search',
            'position': 1,
            'pageNum': p
        }
        res = requests.get(url, params=params).json()
        print(res)
        with(open('data.json', 'w')) as fl:
            json.dump(res, fl)
        stock_data = res['data']
        for stock in stock_data:
            print(stock)
        print(len(stock_data))

        # //soup = BeautifulSoup(res, features="html.parser")
        # jobs = soup.find('table', attrs={'id': 'DataTables_Table_0'})
        # print(jobs)

        """
        for job in jobs:
            title = job.find('h3').text
            job_url = job.find('a')['href']
            company = job.find('h4').text
            location = job.find('span', attrs={'class': 'job-result-card__location'}).text
            desc = job.find('p').text
            time = job.find('time').text
            job_summary = {'title': title, 'company': company, 'location': location, 'desc': desc, 'time': time,
                           'job_url': job_url}
            job_list.append(job_summary)
        """

    return render_template('linkedin-scrapper.html', jobs=job_list)


@app.route('/<string:pagename>')
def pages(pagename):
    return render_template(f'{pagename}.html')


# @app.errorhandler(404)
# def not_found(e):
#     return render_template("error.html")


@app.errorhandler(Exception)
def not_found(e):
    return render_template("error.html", e=e.code)


if __name__ == "__main__":
    if platform.system() == 'Darwin':
        app.run(debug=True)
    app.run()
