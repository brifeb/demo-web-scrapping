import os
import sys
from flask import Flask

#sys.path.insert(0, os.path.dirname(__file__))

app = Flask(__name__)

@app.route('/')
def index():
    return 'hi ooo uom, coba masukkan'

@app.route('/<string:name>/')
def halo(name):
    return 'halooo bos ' + name

if __name__ == "__main__":
    app.run()