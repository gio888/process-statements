#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import libraries
import os
import pandas as pd
import re
import csv
from io import StringIO
from pathlib import Path


# In[ ]:


#read file
filename = Path(input("Enter the file name : "))


# In[ ]:


#load csv to dataframe
col_list = ['date_raw', 'desc_raw', 'debit_raw', 'credit_raw','bal_raw']
df = pd.read_csv(filename, names = col_list)


# In[ ]:


#clean up date field
new = df["date_raw"].str.split(" ", n = 1, expand = True)

# making separate first name column from new data frame 
df["date"]= new[0] 
  
# making separate last name column from new data frame 
df["desc01"]= new[1] 
  
# Dropping old Name columns 
#df.drop(columns =["Name"], inplace = True)


# In[ ]:


#fill blank dates
df.date = df.date.fillna(method = 'ffill')


# In[ ]:


#drop last 3 rows
df.drop(df.tail(3).index,inplace=True)


# In[ ]:


#fix date
#extract day month year
day = df.date.str.extract(r'(\d{2})', expand = False)
month = df.date.str.extract(r'([A-Za-z]{3})', expand = False)
year = df.date.str.extract(r'(\d{4})', expand = False)
# refill column
df['date'] = pd.to_datetime((month + ' ' + day + ", " + year)).dt.strftime("%m/%d/%Y")


# In[ ]:


#fix desc
#fix nan
df[['desc01','desc_raw']] = df[['desc01','desc_raw']].fillna('') 
#fix \n
df['desc_raw'] = df.desc_raw.str.replace('\n',' ')
df['desc'] = (df.desc01 + ' ' + df.desc_raw).str.lower()


# In[ ]:


#drop unneeded rows
df = df.drop(df[(df.debit_raw.isna() & df.credit_raw.isna())].index)


# In[ ]:


#get rid of NaNs
df = df.fillna(value = 0)


# In[ ]:


#drop unneeded columns
df.drop(['date_raw','desc_raw','bal_raw','desc01'], axis = 1, inplace = True)


# In[ ]:


#rearrage
df = df[['date','desc','debit_raw','credit_raw']]


# In[ ]:


#drop unneeded rows
df = df.loc[-df.debit_raw.str.contains('\n',na=False)]


# In[ ]:


#strip unneeded spaces
df.desc = df.desc.str.strip()
df.desc = df.desc.str.replace(" +"," ")


# In[ ]:


#export to csv
filename_csv_full = 'for import ' + filename.name
export_csv = df.to_csv (filename_csv_full, index = None, header=True)

