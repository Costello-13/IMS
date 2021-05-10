# Scraper_DBA

scraper.py:
Once scraper.py is executed, it will run every 60 seconds until the program is closed.
At each interval (60 seconds), the scraper will go through the website data and search for the highest BTC value.
Then, the hash, timeframe and USD value associated with the highest BTC value will be stored in the scraper.txt file. 

Scraper.txt: 
When no scraper.txt file exists, one will be made automatically. 
When a scraper.txt file exists: output will be appended to the existing scraper.txt file

Note: 
Scraper operates on UTC time zone (currently 2h time difference with Belgium)


*Added just after exam for clarification of python files in Github on 10/05/2021*
DEFINITVE VERSION OF ASSIGNMENT: 
The python file 'defscraper' is the final version of the Scraper, which scrapes the data from the website and sends it to Redis. 
the python file 'Parser' then gets this data out of Redis and sends the highest value to MongoDB. 
These 2 files run every 60 seconds. 

MONGO: 
I made a database called "btc_scraper" in MongoDB. 

REDIS: 
The defscraper.py file sends ALL the scraped data to the Redis cache every 60 seconds. When new data enters this cache, the old data is deleted. 
the parser.py file pulls ALL the scraped data from the Redis cache (in the form of bytes) and transforms it back into a dictionary, so it can be pushed to the MongoDB. 

DOCKER:
I made 2 images on Ubuntu, one for the Scraper and one for the Parser. I pushed these to dockerhub. On my default operating system (MacOS), I then pulled 5 images, 3 of them official images (Ubuntu, Mongo and Redis) and then my own 2 (Scraper and Parser). 

I ran all these images, so they would become a container on my operating system. Afterwards I put all these 5 images in a network (btc), which I created in docker with the command "docker network connect btc *container*" 

This way, all my containers run in the same network. 

After I start the containers, I open MongoDB Compass to verify that the highest value enters the database. 

