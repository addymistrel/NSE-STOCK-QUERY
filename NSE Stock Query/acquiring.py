import requests
import zipfile
import sqlite3
import pandas as pd
from pathlib import Path
import os,glob
import datetime
import io
import shutil
import csv
from jugaad_data.nse import bhavcopy_save
from jugaad_data.holidays import holidays
from urllib import request
import queries

#For Security CSV File
get_req = requests.get("https://archives.nseindia.com/content/equities/EQUITY_L.csv")
contents = get_req.content
ssc = pd.read_csv(io.StringIO(contents.decode('utf-8')))
df2 = pd.DataFrame(ssc)
df2.to_csv("security.csv",index=False)

#For BhavCopy CSV File
link = 'https://archives.nseindia.com/content/historical/EQUITIES/2022/DEC/cm08DEC2022bhav.csv.zip'

request.urlretrieve(link, 'cm08DEC2022bhav.csv.zip')
with zipfile.ZipFile('cm08DEC2022bhav.csv.zip') as z:
    with z.open('cm08DEC2022bhav.csv') as f:
        data = pd.read_csv(f)
        df = pd.DataFrame(data)
        df.drop(columns=['Unnamed: 13'],inplace=True)
        df.to_csv("bhavcopy.csv",index=False)
path = "C:/Users/addym/OneDrive/Desktop/Python Internship/"
os.remove('cm08DEC2022bhav.csv.zip')

#Creating a folder for all bhavcopy of last 30 days
pp = os.path.dirname(os.path.abspath(__file__))
datapath = os.path.join(pp,"bhavcopy_data")
if not os.path.exists(datapath):
    os.mkdir(datapath)

#Getting current date and 30 days previous date
start = datetime.datetime.today().strftime('%m/%d/%Y')
end = (datetime.datetime.today() - datetime.timedelta(days=30)).strftime('%m/%d/%Y')

#saving all bhavcopies of last 30 days
date_range = pd.bdate_range(start=end,end=start,freq= 'C', holidays=holidays(2022))
for dates in date_range:
    bhavcopy_save(dates, datapath)

#Creating a database
Path('database.db').touch()
#Getting Column names of both database
security_col = list(df.columns)
bhav_col = list(df.columns)
print(security_col)
print(bhav_col)

conn = sqlite3.connect("database.db")
c = conn.cursor()
c.execute("create table if not exists security ({}, {}, {}, {}, {}, {}, {}, {})" .format(*security_col))
c.execute("create table if not exists bhavcopy({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})" .format(*bhav_col))
c.execute("create table if not exists bhavcopy_30days({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})" .format(*bhav_col))

#Inserting Data in Database
#Security
ctr=0
with open("security.csv",'r') as csvfile:
    for row in csvfile:
        if ctr==0:
            ctr=1
            pass
        c.execute("insert into security values (?,?,?,?,?,?,?,?)", row.split(","))
        conn.commit() 
#bhavcopy
ctr=0
with open("bhavcopy.csv",'r') as csvfile:
    for row in csvfile:
        if ctr==0:
            ctr=1
            pass
        c.execute("insert into bhavcopy values (?,?,?,?,?,?,?,?,?,?,?,?,?)", row.split(","))
        conn.commit() 

#combining all data of past 30 days in 1 csv file
list_of_bhavcopies=glob.glob(os.path.join(datapath,"*bhav.csv"))
new_df = pd.DataFrame()
for files in list_of_bhavcopies:
    xrr = pd.read_csv(files)
    xrr.drop(columns=['Unnamed: 13'],inplace=True)
    xrr.columns = xrr.columns.str.replace(' ','')
    xrr = xrr.apply(lambda x:x.str.strip() if x.dtype == 'object' else x)
    xrr['TIMESTAMP'] = pd.to_datetime(xrr['TIMESTAMP'])
    new_df = new_df.append(xrr)
new_df.to_csv("bhavcopy30.csv",index=False)

#Inserting in Bhavcopy30 table
ctr=0
with open("bhavcopy30.csv",'r') as csvfile:
    for row in csvfile:
        if ctr==0:
            ctr=1
            pass
        c.execute("insert into bhavcopy_30days values (?,?,?,?,?,?,?,?,?,?,?,?,?)", row.split(","))
        conn.commit()

#RUNNING QUERIES

queries.query1(bhav_col)
queries.query2(bhav_col)
queries.query3(bhav_col)

c.close
conn.close()



