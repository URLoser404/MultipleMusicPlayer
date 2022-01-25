from flask import *
import search.py




app = Flask(__name__)


@app.route('/')
def main():
    return  render_