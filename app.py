from flask import Flask, render_template, request
import requests, json
from bs4 import BeautifulSoup
import math, os

def millify(n):
    millnames = ['', ' k', ' m', ' b', ' t']
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.2f}{}'.format(n / 10**(3 * millidx), millnames[millidx])


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/steam')
def steam_parser():
    url = 'https://store.steampowered.com/games#p=0&tab=TopSellers'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
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

    return render_template('detik-scrapper.html', gambars = gambars)

@app.route('/usd-rates')
def idr_rates():
    source = requests.get('http://www.floatrates.com/daily/usd.json')
    json_data = source.json()
    return render_template('rates-scrapper.html', datas = json_data.values())

@app.route('/instagram')
def instagram():
    headers = {
        'cookie': 'csrftoken=tCnfL3s9LPVnJKyBsUB2zNTRfXN7ZIMF; ig_did=83F3627C-09E1-4CD6-8C7F-D52B90C882C7; ig_nrcb=1; mid=XGo2dQAEAAG1yHcB9Z8SxuXLq16Q',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'
    }
    ig_users = ['brifeb', 'valeyellow46', 'leomessi', 'gianluigibuffon', 'cristiano', 'marcmarquez93']
    users = []
    for usr in ig_users:
        url = f'https://www.instagram.com/{usr}/?__a=1'
        res = requests.get(url, headers=headers).json()
        users.append(res['graphql']['user'])
    return render_template('ig-scrapper.html', datas = users)

@app.route('/igtopnine')
def igtopnine():
    # update_img = request.args.get('update') or False
    username = 'valeyellow46'

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(PROJECT_ROOT, "data")


    with(open(f'{DATA_DIR}/{username}.json', 'r')) as fl:
        profile = json.load(fl)
    with(open(f'{DATA_DIR}/{username}-top9comments.json', 'r')) as fl:
        top_9_comm = json.load(fl)
    with(open(f'{DATA_DIR}/{username}-top9likes.json', 'r')) as fl:
        top_9_likes = json.load(fl)

    top9like_img = []
    top9comm_img = []
    for i in range(9):
        top9like_img.append(f'/static/img/{username}/{username}-{i+1}-top9likes.jpg')
        top9comm_img.append(f'/static/img/{username}/{username}-{i+1}-top9comments.jpg')

    print(top9comm_img)

    return render_template('ig-topnine.html',
                           profile = profile,
                           toplikes=zip(top_9_likes,top9like_img),
                           topcomments=zip(top_9_comm,top9comm_img),
                           millify=millify)

@app.route('/twitter')
def twitter():
    username = 'ladbible'
    size_thumb = 3

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(PROJECT_ROOT, "data/")

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
        jobs = soup.findAll('li', attrs={'class': 'result-card'})
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
    # app.run(debug=True)
    app.run()