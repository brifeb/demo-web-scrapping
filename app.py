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

@app.route('/instagram')
def instagram():
    headers = {'cookie': 'mid=W2b0DAAEAAFbGydJZW58lOkhgeoZ; ig_did=80108C7D-D4E0-4DCE-98D3-B74C5A991B81; fbm_124024574287414=base_domain=.instagram.com; ig_nrcb=1; ds_user_id=11167978215; csrftoken=H0wnh0uPuP6R4zUrW727nq8ac253Zj29; sessionid=11167978215:4RS02ZBaFnXSDz:26; shbid=155; shbts=1613612901.0640295; rur=FRC; fbsr_124024574287414=VESKTm5jd6jzo_PmkqEtzROrAvd2BYMyBzNoWDBUVxk.eyJ1c2VyX2lkIjoiMTI0OTgzMzI4MiIsImNvZGUiOiJBUUFsNjZyM0VCWHFFWGdvajNyc1dvdHRCdkg2a1pkQkJfN19vcnRLekNEbmkySnZIWHhwQnQtM3pqWVhhdVFiY001eHpib2tDQVNGLUlaS2t3Sk1DaV9NUmk5SXk1THBYNUstUVhueUtYajI2N0JEQnhJbW80WE41U3BWS1BpUk9FOE5hTUJIcC1raWFjV1k1N0VzNUxVYjRwb0Q4b3NEdzJxVU9GMnhTbUFNOGhVY25jOTU1VGhhQWtYNGdCZy1HRUJyaFF5alhPU0loLXBleE5WSmx4SDdpRUp0ZjhyNjRqaUVUWVpVckk5ZGtKR0lYUEhXeXpxLXQyNWFRNWhaQ0RZeV9XLXNsQ0k3bEFoQkc1d0hMV25kSmJEYlpoWC1lUmdkSHJaQk1jS1Y2bGdTSV9zS2lFSjVyS0toWVcyWmE2dyIsIm9hdXRoX3Rva2VuIjoiRUFBQnd6TGl4bmpZQkFIcVpDdkl4ZVZJd0hxTEtuRm5xclpDaXZITXA2bkI4VFRiOFNNbFpCY0Z4WVJoSG9aQnVyMmU0VE0xekpQRmdoVkhqdDVaQTRrWkNoZDR3a3FlSUNoS3o4UU0ybTZhem03ejlPZ2ZzdVpBRFVMOE4xbmw0UmRyYTJEZEo1RW93SllOQUZCUklib216Mm12M3kzUWVMTldaQ1ZsNE9WZHVkb0xpTUFJTDFTSTZ2TG1ETTQ0b2tuSVpEIiwiYWxnb3JpdGhtIjoiSE1BQy1TSEEyNTYiLCJpc3N1ZWRfYXQiOjE2MTM4MzcwOTF9'}
    ig_users = ['brifeb', 'cristiano', 'leomessi', 'gianluigibuffon', 'zidane']
    users = []
    for usr in ig_users:
        url = f'https://www.instagram.com/{usr}/?__a=1'
        res = requests.get(url, headers=headers).json()
        users.append(res['graphql']['user'])
    return render_template('ig-scrapper.html', datas = users)

@app.route('/<string:pagename>')
def pages(pagename):
    return render_template(f'{pagename}.html')

if __name__ == "__main__":
    app.run()