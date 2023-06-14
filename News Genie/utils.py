import mysql.connector
import traceback
from models import *

# Function is called with scraper.py to store the data in the database
def storing_data_scraper(data):
    try:
        print("Storing in a Database.....")
        mydb = mysql.connector.connect(host="localhost",user="root",password="Sidhant!996",database="summarizer")
        mycursor = mydb.cursor()
        i = 1
        print(data)
        for article in data:
            print(f"Storing the {i} article")
            query = "INSERT INTO articles (Article, Synopsis, DatePublished, ArticleLink) VALUE (%s, %s, %s, %s)"
            mycursor.execute(query, article)
            i = i + 1
        mydb.commit()
        mycursor.close()
        mydb.close()
        print("Finishing the Storing Procedure")
    except:
        traceback.print_exc()
        print("Cannot Connect to Database!!!!")

# Getting the data from the database where the data is NULL
def getting_data():
    try:
        print("Getting data from a Database.....")
        mydb = mysql.connector.connect(host="localhost",user="root",password="Sidhant!996",database="summarizer")
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM articles WHERE PredictedSummary IS NULL")
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        print("Finishing the GET Process")
        return result
    except:
        traceback.print_exc()
        print("Cannot connect to database!!!")

# Predicting the Summary and headline
def predicting_data():
    result = getting_data()
    predicted_data = []
    # Predicting the Summary
    for article_id, input_text, synopsis, heading1, heading2, heading3, PredSummary, pub, article_link in result:
        print("Predicting the Summary....")
        predictedSummary = BART_summary(input_text)
        print("Predicting the Heading 1....")
        heading1 = BART_headline(input_text)
        print("Predicting the Heading 2....")
        heading2 = T5_Headline(input_text)
        print("Predicting the Heading 3....")
        heading3 = BERT_headline(input_text)

        predicted_data.append((predictedSummary, heading1, heading2, heading3, article_id))

    print("Prediction is completed!!!")
    return predicted_data


# Storing the Prediction data back to the database
def storing_prediction_data():
    result_data = predicting_data()
    try:
        print("Storing the Predicted Data")
        mydb = mysql.connector.connect(host="localhost",user="root",password="Sidhant!996",database="summarizer")
        mycursor = mydb.cursor()
        i = 1
        print(result_data)
        query = "UPDATE articles SET PredictedSummary = %s, Heading1 = %s, Heading2 = %s, Heading3 = %s WHERE ArticleId = %s"
        for article in result_data:
            print(f"Storing the {i} article")
            mycursor.execute(query, article)
            mydb.commit()    
            i = i + 1
        mycursor.close()
        mydb.close()
        print("Finishing the Storing Procedure")
    except:
        traceback.print_exc()
        print("Cannot Connect to Database!!!")


# Getting the predicted data
def getting_predicted_data():
    storing_prediction_data()
    try:
        print("Getting data from a Database.....")
        mydb = mysql.connector.connect(host="localhost",user="root",password="Sidhant!996",database="summarizer")
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM articles LIMIT 4")
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        print("Finishing the GET Process")
        return result
    except:
        traceback.print_exc()
        print("Cannot connect to database!!!")

getting_predicted_data()

def final_output_front():
    try:
        print("Getting data from a Database.....")
        mydb = mysql.connector.connect(host="localhost",user="root",password="Sidhant!996",database="summarizer")
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM articles WHERE DatePublished = '19 Apr, 2023'")
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        print("Finishing the GET Process")
        return result
    except:
        traceback.print_exc()
        print("Cannot connect to database!!!")