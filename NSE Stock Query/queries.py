import sqlite3
import pandas as pd
conn = sqlite3.connect("database.db")
c = conn.cursor()

def query1(col):
    c.execute('''select * from bhavcopy order by gain desc limit 25 ''')
    newdf = pd.DataFrame(c.fetchall(),columns=col)
    newdf.to_csv("query1.csv",index=False)

def query2(col):
    c.execute('''select * from bhavcopy_30days order by gain desc limit 750''')
    newdff = pd.DataFrame(c.fetchall(),)
    newdff.to_csv("query2.csv",index=False)

def query3(col):
    c.execute('''select * from bhavcopy_30days order by gain desc limit 25 ''')
    newdfff = pd.DataFrame(c.fetchall(),columns=col)
    newdfff.to_csv("query3.csv",index=False)
