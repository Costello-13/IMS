import requests, pprint, sched, time, pymongo, redis
from bs4 import BeautifulSoup

mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
mongodb = mongoclient["btc_database"]
mongocol = mongodb["btc_scraper"]

connection = redis.StrictRedis(host="localhost", port=6379, db=0)

data = connection.get("df")
print(data)