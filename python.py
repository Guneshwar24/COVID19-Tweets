import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup as BS
from prettytable import PrettyTable
import os
import numpy as np
import matplotlib.pyplot as plt
import twarc
import tweepy
import re

def get_info(url):
	data = requests.get(url)
	soup = BS(data.text, 'html.parser')
	total = soup.find("div", class_ = "maincounter-number").text
	
	total = total[1 : len(total) - 2]
	other = soup.find_all("span", class_ = "number-table")
	recovered = other[2].text
	deaths = other[3].text
	deaths = deaths[1:]
	ans ={'Total Cases' : total, 'Recovered Cases' : recovered,
								'Total Deaths' : deaths}

	return ans

url = "https://www.worldometers.info/coronavirus/"
ans = get_info(url)


def live_count():

    url = 'https://www.mohfw.gov.in/'

    web_content = requests.get(url).content

    soup = BeautifulSoup(web_content, "html.parser")

    extract_contents = lambda row: [x.text.replace('\n', '') for x in row]

    stats = [] 
    all_rows = soup.find_all('tr')
    for row in all_rows:
        stat = extract_contents(row.find_all('td')) 
        if len(stat) == 5:
            stats.append(stat)

    new_cols = ["Sr.No", "States/UT","Confirmed","Recovered","Deceased"]
    state_data = pd.DataFrame(data = stats, columns = new_cols) 

    return state_data


def Real_time():
    userID ="covid19indiaorg"
    consumer_key = "e74JGuc5t5MYEQRVbvsQZcp62"
    consumer_secret = "MmybENPWhesKwKhZ5kIwagZyiYVarXbHJ4I9v7Cdbhci4LESp0"
    access_token = "768133015285268480-BHvFD0WFD67IEMoRA7jsk9AReNv9683"
    access_token_secret = "6z1uM4JODyn60wdQTyde9IS8URJrbQlFSZdfG2IntJtIW"
    t = twarc.Twarc(consumer_key, consumer_secret, access_token, access_token_secret) 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name=userID, 
                            # 200 is the maximum allowed count
                            count=200,
                            include_rts = False,
                            # Necessary to keep full_text 
                            # otherwise only the first 140 words are extracted
                            tweet_mode = 'extended'
                            )
    for info in tweets[:3]:
        print("ID: {}".format(info.id))
        print(info.created_at)
        print(info.full_text)
        print("\n")
    all_tweets = []
    all_tweets.extend(tweets)
    oldest_id = tweets[-1].id
    while True:
        tweets = api.user_timeline(screen_name=userID, 
                            # 200 is the maximum allowed count
                            count=200,
                            include_rts = False,
                            max_id = oldest_id - 1,
                            # Necessary to keep full_text 
                            # otherwise only the first 140 words are extracted
                            tweet_mode = 'extended'
                            )
        if len(tweets) == 0:
            break
        oldest_id = tweets[-1].id
        all_tweets.extend(tweets)
        print('N of tweets downloaded till now {}'.format(len(all_tweets)))

    from pandas import DataFrame
    outtweets = [[tweet.id_str, 
                tweet.created_at, 
                tweet.favorite_count, 
                tweet.retweet_count, 
                tweet.full_text.encode("utf-8").decode("utf-8")] 
                for idx,tweet in enumerate(all_tweets)]
    df = DataFrame(outtweets,columns=["id","created_at","favorite_count","retweet_count", "text"])
    df.to_csv('%s_tweets.csv' % userID,index=False)
    df.head(3)

    return all_tweets

def remove_tags(str):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",str).split())