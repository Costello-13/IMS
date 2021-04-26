import requests, pprint
from bs4 import BeautifulSoup
import pandas as pd
request = requests.get("https://www.blockchain.com/btc/unconfirmed-transactions")
#print(request.status_code)

soup = BeautifulSoup(request.text, "html.parser")
tags = soup.findAll('div', attrs={"class": "sc-1g6z4xm-0 hXyplo"})
hashes = []
attrlist = []

for tag in tags: 
    bchash = tag.findAll('a', attrs={"class": "sc-1r996ns-0 fLwyDF sc-1tbyx6t-1 kCGMTY iklhnl-0 eEewhk d53qjk-0 ctEFcK"})
    for i in bchash:
        #print(i.text)
        hashes.append(i.text)
    
    attributes = tag.findAll('span', attrs={"class": "sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC"})
    for i in attributes:
        attrlist.append(i.text + " ")
transactionslist = []
# for i in range(len(hashes)): 
    # one = []
    # one.append(hashes[i])
    # one.append(attrlist[i])
    # one.append(attrlist[i+1])
    # one.append(attrlist[i+2])
    # transactionslist.append(one)
# pprint.pprint(transactionslist)
timelist = [] 
btclist = [] 
usdlist = []
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
    diccybtc[hashes[i]] = btclist[i]
    diccyusd[hashes[i]] = usdlist[i]

for i in range(len(hashes)): 
    one = [] 
    one.append(hashes[i])
    one.append(timelist[i])
    one.append(btclist[i])
    one.append(usdlist[i])
    transactionslist.append(one)
#print(transactionslist)
# combinedlist = [attrlist[i] + attrlist[i+1] + attrlist[i+2] for i in range(0, len(attrlist), 3)]
# print(transactionslist)

df = pd.DataFrame(transactionslist, columns=["hash", "time", "BTC", "USD"])

print(df)
