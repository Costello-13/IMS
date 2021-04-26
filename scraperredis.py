
Skip to content
Pull requests
Issues
Marketplace
Explore
@Costello-13
Costello-13 /
IMS

1
0

    0

Code
Issues
Pull requests
Actions
Projects
Wiki
Security
Insights

    Settings

IMS/testredis.py /
@Costello-13
Costello-13 Add files via upload
Latest commit 0185296 32 minutes ago
History
1 contributor
92 lines (72 sloc) 3.4 KB
import requests, pprint, sched, time, pymongo, redis, pickle, zlib
from bs4 import BeautifulSoup
import pandas as pd

############################################################################################
# MongoDB
############################################################################################
mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
mongodb = mongoclient["btc_database"]
mongocol = mongodb["btc_scraper"]

###########################################################################################
# Redis
###########################################################################################
r = redis.StrictRedis(host="localhost", port=6379, db=0)
############################################################################################
# Scraper
############################################################################################
s = sched.scheduler(time.time, time.sleep)
def btcscraper(sc): 
    request = requests.get("https://www.blockchain.com/btc/unconfirmed-transactions")
    soup = BeautifulSoup(request.text, "html.parser")
    tags = soup.findAll('div', attrs={"class": "sc-1g6z4xm-0 hXyplo"})
    hashes = []
    attrlist = []

    #scraper_file = open('scraper.txt', 'a')


    for tag in tags: 
        bchash = tag.findAll('a', attrs={"class": "sc-1r996ns-0 fLwyDF sc-1tbyx6t-1 kCGMTY iklhnl-0 eEewhk d53qjk-0 ctEFcK"})
        for i in bchash:
            #print(i.text)
            hashes.append(i.text)
    
        attributes = tag.findAll('span', attrs={"class": "sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC"})
    
        for i in attributes:
            attrlist.append(i.text + " ")


    # combinedlist = [attrlist[i] + attrlist[i+1] + attrlist[i+2] for i in range(0, len(attrlist), 3)]

    timelist = [] 
    btclist = [] 
    usdlist = []
    transactionslist = []
    diccybtc = {}
    diccyusd = {}

    for i in range(0, len(attrlist), 3): 
        temp = attrlist[i].replace(' ', '')
        timelist.append(temp)
    for i in range (1, len(attrlist), 3):
        temp= attrlist[i].rstrip("BTC ")
        btclist.append(float(temp))

    for i in range(2, len(attrlist), 3): 
        temp = attrlist[i].replace('$','')
        temp2 = temp.replace(' ', '')
        temp3 = temp2.replace(',', '')
        usdlist.append(float(temp3))
    for i in range(len(hashes)): 
        one = [] 
        one.append(hashes[i])
        one.append(timelist[i])
        one.append(btclist[i])
        one.append(usdlist[i])
        transactionslist.append(one)
    
    
    df = pd.DataFrame(transactionslist, columns=["hash", "time", "BTC", "USD"])
    r.setex("key", 60, zlib.compress(pickle.dumps(df)))

    btclist.sort(reverse=True)
    usdlist.sort(reverse=True)

    for key, value in diccybtc.items():
        if diccybtc[key] == btclist[0]:
            #print("Hash:", key, "Time:", timelist[0], "BTC value:", value, "USD value:", diccyusd[key])
            text = " Hash: " + key + " Time: " + timelist[0] + " BTC value: " + str(value) + " USD value: " +  diccyusd[key]
            #scraper_file.write(text)
            #scraper_file.write("\n")
            diccymongo = {"hash": key, "Time": timelist[0], "BTC_value": str(value), "USD_value": diccyusd[key] }
            x = mongocol.insert_one(diccymongo)
    s.enter(60, 1, btcscraper, (sc,))

s.enter(60, 1, btcscraper, (s,))
s.run()


 

    © 2021 GitHub, Inc.
    Terms
    Privacy
    Security
    Status
    Docs

    Contact GitHub
    Pricing
    API
    Training
    Blog
    About

Loading complete