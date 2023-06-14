import pandas as pd
import requests
from bs4 import BeautifulSoup
from utils import *

data = pd.read_csv("Data/List.csv")
base_url = "https://economictimes.indiatimes.com/archivelist"

def day_links(year, month, starttime, endtime):
    links = []
    for i in range(int(starttime),int(endtime)):
        day_link=f"{base_url}/year-{str(year)},month-{str(month)},starttime-{str(i)}.cms"
        links.append(day_link) 
    return links

def get_url(url):
    headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    cookies = {'session-id':'130-2350219-8238762'}
    return requests.get(url, {'headers':headers})

def one_day(link):
    article_links = []
    soup=BeautifulSoup(get_url(link).text,'html.parser')
    date_pub=soup.find_all('b')[1].text
    for ultag in soup.find_all('ul', class_= 'content'):
        for litag in ultag.find_all('li'):
            for atag in litag.find_all('a'):
                if(atag.get('href')!='#'):
                    link_reqd = "https://economictimes.indiatimes.com" + atag.get('href')
                    article_links.append(link_reqd)
    return article_links, date_pub

def serial(serial_number):
    temp = data.loc[data['Serial_Number'] == serial_number]
    year = int(temp.Year)
    month = int(temp.Month)
    start = int(temp.R1)
    end = int(temp.R2)
    return [year,month,start,end]

def scraper(url):
    dict_day = {'date_published':[], 'headline':[], 'synopsis':[], 'full_text':[], 'article_link':[]}
    # dict_day = {'full_text':[], 'synopsis':[], 'date_published':[], 'article_link':[]}
    article_links, date_pub = one_day(url)
    dict_scraper = []
    i = 0
    for link in article_links[0:6]:
        print("Scraping the Link")
        soup=BeautifulSoup(get_url(link).text,features='html.parser')

        # Getting Headline and Date Published
        try:
            print("Getting Headline and Date Published!!!")
            dict_day['date_published'].append(date_pub)
            dict_day['article_link'].append(link)
        except:
            print("Getting date and Headline Failed")
            continue
        
        # Getting Synopsis
        try:
            print("Getting the Summary")
            dict_day['synopsis'].append(soup.find('h2',class_="summary").text)
        except:
            # dict_day['synopsis'].append('NA')
            continue

        # Getting the Article
        try:
            print("Getting the Article")
            partial_text=soup.find('article',class_='artData clr').text
            all_text=partial_text[:partial_text.find("Experience Your Economic Times")-21]
            dict_day['full_text'].append(all_text)
        except:
            try :
                print("Still trying to get the Article")
                some_text=soup.find('article',class_='artData clr paywall').text
                final_text=some_text[:some_text.find("Experience Your Economic Times")-23]
                dict_day['full_text'].append(final_text)
            except:
                print("Article can not be gathered")
                dict_day['full_text'].append('NA')
                continue
        
        # Appending the results
        dict_scraper.append((dict_day['full_text'][i], dict_day['synopsis'][i], date_pub, link))
        i += 1
    print("Returning the data")
    return dict_scraper

for i in range(182, 183):
  year, month, starttime, endtime = serial(i)
  print(f"Year : {year}, Month: {month}")
  links = day_links(year, month, starttime, endtime)
  print(len(links))
  for url in links[0:1]:
    print("Scraping Started")
    data = scraper(url)
    print("Scraping Ended")

storing_data_scraper(data)
