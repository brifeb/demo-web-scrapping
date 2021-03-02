from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

#sys.path.insert(0, os.path.dirname(__file__))

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

@app.route('/idr-rates')
def idr_rates():
    source = requests.get('http://www.floatrates.com/daily/idr.json')
    json_data = source.json()
    return render_template('rates-scrapper.html', datas = json_data.values())

@app.route('/<string:pagename>')
def pages(pagename):
    return render_template(f'{pagename}.html')

if __name__ == "__main__":
    app.run()