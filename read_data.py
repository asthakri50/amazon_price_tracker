import sqlite3
import pandas as pd

#connect to/create database
conn = sqlite3.connect('amz_price_tracker.db')

df = pd.read_sql_query(''' SELECT * FROM prices''' , conn)

print(df)
