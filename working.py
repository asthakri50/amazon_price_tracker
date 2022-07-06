from socket import timeout
from tkinter.tix import TEXT
from requests_html import HTMLSession
import csv
import datetime
import sqlite3

#connect to/create database
conn = sqlite3.connect('amz_price_tracker.db')
c = conn.cursor()
#c.execute(''' CREATE TABLE prices(date DATE , asin TEXT , price FLOAT , title TEXT) ''' )


#start sesion and create lists
s = HTMLSession()
asins = []

#read csv to list
with open('asins.csv' , 'r') as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        asins.append(row[0])

#scrap data
for asin in asins:
    r = s.get(f'https://www.amazon.in/dp/{asin}')

    r.html.render(timeout=20)
    try:
        price = r.html.find('.a-offscreen')[0].text.replace('₹','').replace(',','').strip()
    except:
        price = '₹ 0.00'    

    title = r.html.find('#productTitle')[0].text.strip()
    asin = asin
    date = datetime.datetime.today()
    
    c.execute(''' INSERT INTO prices VALUES(?,?,?,?)''', (date , asin , price , title) )
    print(f'Added data for {asin} , {price}')

conn.commit()
print('Committed new entries to database')




