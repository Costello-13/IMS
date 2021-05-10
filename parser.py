
import requests, pprint, sched, time, pymongo, redis, json
from bs4 import BeautifulSoup
import pandas as pd

mongoclient = pymongo.MongoClient("mongodb://localhost:27017/") ### Werkt niet in Docker --> in pythonfile veranderd naar "mongodb://172.17.0.3:27017/" voor connectie in Docker
mongodb = mongoclient["btc_database"]
mongocol = mongodb["btc_scraper"]

connection = redis.StrictRedis(host="localhost", port=6379, db=0) #"localhost" werkt niet in Docker --> veranderd naar "redis"

s = sched.scheduler(time.time, time.sleep)


def btcparser(sc):
	data = connection.get("df")

	str_data = data.decode('UTF-8')
	data_json = json.loads(str_data)

	data_df = pd.DataFrame(data_json)

	#for row in data_df.iterrows():
	#print(row)

	data_df.reset_index(inplace=True)
	data_df.sort_values(by=['USD'],inplace=True, ascending=False)

	data_diccy = data_df.to_dict("records")

	for x in range(0,1):
		mongocol.insert_one(data_diccy[x])
	s.enter(60,1, btcparser, (sc,))
s.enter(60,1,btcparser, (s,))
s.run()
