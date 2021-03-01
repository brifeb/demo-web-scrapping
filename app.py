from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

#sys.path.insert(0, os.path.dirname(__file__))

app = Flask(__name__)

@app.route('/')
def home():
    return 'halooo'

if __name__ == "__main__":
    app.run()