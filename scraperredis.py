import requests, pprint, sched, time, pymongo, redis
from bs4 import BeautifulSoup

############################################################################################
# MongoDB
############################################################################################
mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
mongodb = mongoclient["btc_database"]
mongocol = mongodb["btc_scraper"]

###########################################################################################
# Redis
###########################################################################################
client = redis.Redis(host= 'ipaddr', port = 6379)

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
            #client.sadd('hasheslist', i.text)
    
        attributes = tag.findAll('span', attrs={"class": "sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC"})
    
        for i in attributes:
            attrlist.append(i.text + " ")
            #client.sadd('attributeslist', i.text + " ")


    combinedlist = [attrlist[i] + attrlist[i+1] + attrlist[i+2] for i in range(0, len(attrlist), 3)]

    for i in combinedlist:
        client.sadd('redislist', i)

    timelist = [] 
    btclist = [] 
    usdlist = []
    diccybtc = {}
    diccyusd = {}

    for i in range(0, len(attrlist), 3): 
        timelist.append(attrlist[i])

    for i in range (1, len(attrlist), 3):
        temp= attrlist[i].rstrip("BTC ")
        btclist.append(float(temp))

    for i in range(2, len(attrlist), 3): 
        usdlist.append(attrlist[i])

    for i in range(len(hashes)):
        diccybtc[hashes[i]] = btclist[i]
        diccyusd[hashes[i]] = usdlist[i]

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


 