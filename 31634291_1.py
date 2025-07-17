import requests
from bs4 import BeautifulSoup
import os
import re
from pymongo import MongoClient

yahoo_page = requests.get('https://finance.yahoo.com/markets/stocks/most-active/', headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'})
html_file_path = "./yahoo.html"



# used to check status code
# print(yahoo_page.status_code)


if os.path.exists(html_file_path):
    os.remove(html_file_path)

fd = open(html_file_path, "wb")

if yahoo_page.status_code == 200:
    fd.write(yahoo_page.content)
    print("Web page has been stored successfully")
else:
    print("Web page has not been received successfully")
    exit()

fd.close()

fd = open(html_file_path)
soup = BeautifulSoup(fd, "html.parser")

records = soup.find_all('tr', {'class': 'row yf-1570k0a'})
formattedrecords = []


for record in records:
    sparedictionary = dict()
    sparedictionary["index"] = len(formattedrecords)+1
    sparedictionary["symbol"] = record.find('span', {'class': 'symbol'}).contents[0].strip()
    sparedictionary["name"] = record.find('div', {'class': 'leftAlignHeader'}).contents[0].strip()
    sparedictionary["price"] = float(record.find('fin-streamer').contents[0].strip())
    sparedictionary["change"] = float(record.find_all('span', {'class': re.compile("^txt")})[0].contents[0].strip())
    sparedictionary["volume"] = float(record.find('fin-streamer', {"data-field": "regularMarketVolume"}).contents[0].strip()[:-1])
    sparedictionary["volumeunit"] = record.find('fin-streamer', {"data-field": "regularMarketVolume"}).contents[0].strip()[-1]
    formattedrecords.append(sparedictionary)

# print(formattedrecords)
'''
print(record.find('span', {'class': 'symbol'}).contents[0].strip(), end=" ")
print(record.find('div', {'class': 'leftAlignHeader'}).contents[0].strip(), end=" ")
print(record.find('fin-streamer').contents[0].strip(), end=" ")
print(record.find_all('span', {'class': re.compile("^txt")})[0].contents[0].strip(), end=" ")
print(record.find('fin-streamer', {"data-field": "regularMarketVolume"}).contents[0].strip(), end="\n")
'''
 #formattedrecords.append({"index": len(formattedrecords) + 1, "symbol": record.td.div.span.a.div.span.contents[0].strip())

'''
format for documents

multiple documents (records) make a collection


{
    index: 1;
    symbol: "TWTR",
    name: "Twitter, Inc.", 
    price: 51.70,
    change: +2.77
    volume: 172.65M 
}

'''

client = MongoClient("mongodb://localhost:27017")
# dblist = client.list_database_names()
database = client['yahoofinance']
stocks = database['stocks']
stocks.insert_many(formattedrecords)


