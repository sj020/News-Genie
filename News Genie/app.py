from utils import *
from models import *
from flask import Flask, render_template, url_for
import pandas as pd
import random
import requests
from bs4 import BeautifulSoup
from transformers import BartTokenizer, BartForConditionalGeneration
from utils import final_output_front
from flask import Flask, render_template, request

date_pub = []
list_summary = []
full_article_link = []
head1 = []
head2 = []
head3 = []

app = Flask(__name__)
@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/channels')
def channel():
    return render_template("channel.html")

@app.route('/members')
def members():
    return render_template("members.html")

@app.route('/news', methods = ['POST', 'GET'])
def news():
    data = final_output_front()
    for article_id, input_text, synopsis, heading1, heading2, heading3, PredSummary, pub, article_link in data:
        date_pub.append(pub)
        head1.append(heading1)
        list_summary.append(PredSummary)
        full_article_link.append(article_link)
    return render_template("news.html", summary = list_summary, date = date_pub, headline = head1, article_link = full_article_link)

@app.route('/heading1')
def heading1():
    return render_template("news.html", summary = list_summary, date = date_pub, headline = head1, article_link = full_article_link)

@app.route('/heading2')
def heading2():
    data = final_output_front()
    for article_id, input_text, synopsis, heading1, heading2, heading3, PredSummary, pub, article_link in data:
        head2.append(heading2)
    return render_template("news.html", summary = list_summary, date = date_pub, headline = head2, article_link = full_article_link)

@app.route('/heading3')
def heading3():
    data = final_output_front()
    for article_id, input_text, synopsis, heading1, heading2, heading3, PredSummary, pub, article_link in data:
        head3.append(heading3)
    return render_template("news.html", summary = list_summary, date = date_pub, headline = head3, article_link = full_article_link)

if __name__ == "__main__":
    app.run(debug=True, port=8081)
