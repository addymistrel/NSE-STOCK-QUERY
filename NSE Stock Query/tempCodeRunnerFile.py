ctr=0
# with open("security.csv",'r') as csvfile:
#     for row in csvfile:
#         if ctr==0:
#             ctr=1
#             pass
#         c.execute("insert into security values (?,?,?,?,?,?,?,?)", row.split(","))
#         conn.commit() 
# #bhavcopy
# ctr=0
# with open("bhavcopy.csv",'r') as csvfile:
#     for row in csvfile:
#         if ctr==0:
#             ctr=1
#             pass
#         c.execute("insert into bhavcopy values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row.split(","))
#         conn.commit() 

# #combining all data of past 30 days in 1 csv file
# list_of_bhavcopies=glob.glob(os.path.join(datapath,"*bhav.csv"))
# new_df = pd.DataFrame()
# for files in list_of_bhavcopies:
#     xrr = pd.read_csv(files)
#     xrr.drop(columns=['Unnamed: 13'],inplace=True)
#     xrr.columns = xrr.columns.str.replace(' ','')
#     xrr = xrr.apply(lambda x:x.str.strip() if x.dtype == 'object' else x)
#     xrr['TIMESTAMP'] = pd.to_datetime(xrr['TIMESTAMP'])
#     xrr["GAIN"] = (xrr["CLOSE"]-xrr["OPEN"])/xrr["OPEN"]
#     new_df = new_df.append(xrr)
# new_df.to_csv("bhavcopy30.csv",index=False)

# #Inserting in Bhavcopy30 table
# ctr=0
# with open("bhavcopy30.csv",'r') as csvfile:
#     for row in csvfile:
#         if ctr==0:
#             ctr=1
#             pass
#         c.execute("insert into bhavcopy_30days values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row.split(","))
#         conn.commit()

# #RUNNING QUERIES