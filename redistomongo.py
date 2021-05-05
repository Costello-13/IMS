
import requests, pprint, sched, time, pymongo, redis, json
from bs4 import BeautifulSoup
import pandas as pd

mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
mongodb = mongoclient["btc_database"]
mongocol = mongodb["btc_scraper"]

connection = redis.StrictRedis(host="localhost", port=6379, db=0)

data = connection.get("df")

str_data = data.decode('UTF-8')
data_json = json.loads(str_data)

data_df = pd.DataFrame(data_json)

#for row in data_df.iterrows():
	#print(row)

data_df.reset_index(inplace=True)
data_diccy = data_df.to_dict("records")

mongocol.insert_many(data_diccy)
