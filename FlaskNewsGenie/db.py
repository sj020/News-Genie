import pymongo
from models import BART_headline, BART_Summary, BERT_headline, T5_Headline

def storing_data_from_scraper(data):
    try:
        conn = pymongo.MongoClient()
        print("Connection Successfull!!!")
        try:
            db = conn.news_genie
            et_collection = db.economic_times
            article_id = 101
            for article in data:
                temp = {
                    "Article_Id":article_id,
                    "Article":article[0],
                    "Synopsis":article[1],
                    "Published_date":article[2],
                    "Article_link":article[3]
                }
                et_collection.insert_one(temp)
                article_id += 1
            print("Data Stored Successfully!!!")
            conn.close()
        except:
            print("Not able to Store Data.")
    except:
        print("Could not connect to Database.")

def getting_data():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["news_genie"]
        collection_name = db["economic_times"]
        x = collection_name.find()
        data = []
        for article in x:
            data.append(article)
        client.close()
        return data
    except:
        print("Could Not connect to database")

# Predicting the data
def predicting_data():
    result = getting_data()
    for i in result:
        print(f"# Predicting for Article No - {i['Article_Id']}#")
        print("Predicting the BART Summary....")
        bart_summary = BART_Summary(i["Article"])
        print("Predicting the BART Headline....")
        bart_headline = BART_headline(i["Article"])
        print("Predicting the BERT Headline...")
        bert_headline = BERT_headline(i["Article"])
        print("Predicting the T5 Headline...")
        t5_headline = T5_Headline(i["Article"])

        print(f"# Storing the predicted data for Article No - {i['Article_Id']}#")
        storing_predicted_data(i["Article_Id"], bart_summary, bart_headline, bert_headline, t5_headline)


def storing_predicted_data(article_id, bart_summary, bart_headline, bert_headline, t5_headline):
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["news_genie"]
        collection_name = db["economic_times"]
        try:
            collection_name.update_one({"Article_Id":article_id}, {"$set": {"BART_Summary":bart_summary, "BART_Headline":bart_headline,
                                                                            "BERT_Headline":bert_headline, "T5_Headline":t5_headline}})
            client.close()
        except:
            print("Data Not Able to update")
    except:
        print("Not able to connect to database...")





