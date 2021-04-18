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
