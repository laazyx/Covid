import pymongo
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

url = "https://www.worldometers.info/coronavirus/#countries"
URI = "mongodb+srv://admin:admin@covidapp.j3vg0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find("table", id="main_table_countries_today")
get_table_data = table.tbody.find_all("tr")

dic = {}

for i in range(len(get_table_data)):
    try:
        key = get_table_data[i].find_all("a", href=True)[0].string
    except:
        key = get_table_data[i].find_all("td")[0].string

    values = [j.string for j in get_table_data[i].find_all('td')]

    dic[key] = values

column_names = [
    "num", "Countries",
    "Total Cases", "New Cases", "Total Deaths", "New Deaths",
    "Total Recovered", "New Recovered", "Active Cases", "Serious Critical",
    "Tot Cases/1M Pop", "Tot Deaths/1M Pop"
]

df = pd.DataFrame(dic).iloc[:, :].T.iloc[1:, :12]

df.index_name = "Country"

df.columns = column_names #rename column

df.drop('num', inplace=True, axis=1)


# Cleaning DF -----------------------------------------
df = df.fillna("0")
df = df.iloc[:, :7]

df = df.head(200)

for col in df.columns:
    print(col)
    if col != 'Countries':
        df[col] = df[col].str.replace(',', '')
        df[col] = df[col].str.replace('N/A', '0').astype(int)

# print(df.head())

data = df.to_dict(orient="records") #to dic

# print(data)

client = pymongo.MongoClient(URI)

db = client.test

db = client["covid-database"]

print(db)
db.Iris.delete_many({})
db.Iris.insert_many(data)