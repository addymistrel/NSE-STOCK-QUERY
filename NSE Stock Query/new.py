import sqlite3
import pandas as pd
f = pd.read_csv("bhavcopy.csv")
df = pd.DataFrame(f)
df["GAIN"] = (df["CLOSE"]-df["OPEN"])/df["OPEN"]
print(df)