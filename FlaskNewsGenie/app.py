import db
from flask import Flask, render_template
import pandas as pd
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
    data = db.getting_data()
    print(data)
    for i in data:
        date_pub.append(i["Published_date"])
        head1.append(i["BART_Headline"])
        list_summary.append(i["BART_Summary"])
        full_article_link.append(i["Article_link"])
    return render_template("news.html", summary = list_summary, date = date_pub, headline = head1, article_link = full_article_link)

@app.route('/heading1')
def heading1():
    return render_template("news.html", summary = list_summary, date = date_pub, headline = head1, article_link = full_article_link)

@app.route('/heading2')
def heading2():
    data = db.getting_data()
    for i in data:
        head2.append(i["BERT_Headline"])
    return render_template("news.html", summary = list_summary, date = date_pub, headline = head2, article_link = full_article_link)

@app.route('/heading3')
def heading3():
    data = db.getting_data()
    for i in data:
        head3.append(i["T5_Headline"])
    return render_template("news.html", summary = list_summary, date = date_pub, headline = head3, article_link = full_article_link)

if __name__ == "__main__":
    app.run(debug=True, port=8081)

