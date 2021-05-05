import requests
from bs4 import BeautifulSoup
import pprint
import sched
import time

s = sched.scheduler(time.time, time.sleep)
connection = redis.Redis(host='redis', port=6379, db=0)
def btcscraper(sc): 
    request = requests.get("https://www.blockchain.com/btc/unconfirmed-transactions")
    soup = BeautifulSoup(request.text, "html.parser")
    tags = soup.findAll('div', attrs={"class": "sc-1g6z4xm-0 hXyplo"})
    hashes = []
    attrlist = []

    scraper_file = open('scraper.txt', 'a')


    for tag in tags: 
        bchash = tag.findAll('a', attrs={"class": "sc-1r996ns-0 fLwyDF sc-1tbyx6t-1 kCGMTY iklhnl-0 eEewhk d53qjk-0 ctEFcK"})
        for i in bchash:
            #print(i.text)
            hashes.append(i.text)
    
        attributes = tag.findAll('span', attrs={"class": "sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC"})
    
        for i in attributes:
            attrlist.append(i.text + " ")


    combinedlist = [attrlist[i] + attrlist[i+1] + attrlist[i+2] for i in range(0, len(attrlist), 3)]
    print(combinedlist)

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
            scraper_file.write(text)
            scraper_file.write("\n")
    s.enter(60, 1, btcscraper, (sc,))

    ## Redis 
    df = pd.DataFrame(transactionslist, columns=["hash", "time", "BTC", "USD"])
    connection.setex('df', 60, df.to_json())



s.enter(60, 1, btcscraper, (s,))
s.run()


 