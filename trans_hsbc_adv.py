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
col_list = ['date_raw', 'desc_raw', 'credit_raw', 'debit_raw', 'bal_raw']
df = pd.read_csv(filename, names = col_list)


# In[ ]:


#clean up date field
new = df["date_raw"].str.split(" ", n = 1, expand = True)

# making separate first name column from new data frame 
df["date"]= new[0] 
  
# making separate last name column from new data frame 
if new.shape[1] > 1:
    df["desc01"]= new[1]
else:
    df["desc01"]= ''
  


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


#drop unneeded columns
df.drop(['date_raw','desc_raw','bal_raw','desc01'], axis = 1, inplace = True)


# In[ ]:


#fix na of debit and credit rows
df[['credit_raw','debit_raw']] = df[['credit_raw','debit_raw']].fillna(value = 0)


# In[ ]:


#fix missing decimals
if df.debit_raw.dtype == 'O':
    df.debit_raw = df.debit_raw.str.replace(' ','.')
    df.debit_raw = df.debit_raw.str.replace(',','')
    df.debit_raw = df.debit_raw.astype('float')
if df.credit_raw.dtype == 'O':
    df.credit_raw = df.credit_raw.str.replace(' ','.')
    df.credit_raw = df.credit_raw.str.replace(',','')
    df.credit_raw = df.credit_raw.astype('float')


# In[ ]:


#combine rows that needed to be combined
df['flag'] = df.credit_raw + df.debit_raw
bad_row_list = df[df['flag']==0].index.tolist()
for row in bad_row_list:
    df.iloc[row+1] = df.iloc[row] + df.iloc[row + 1]

df = df.drop(bad_row_list) #get rid of bad rows
df = df.drop(columns = 'flag')

#explore later
#df.date.fillna('NaN',inplace=True)
#fund={'date':'first','credit_raw':'sum','debit_raw':'sum','desc':','.join}
#df = df.groupby(df.date.ne(df.date.shift()).cumsum()).agg(fund)


# In[ ]:


#fill blank dates
df.date = df.date.fillna(method = 'ffill')


# In[ ]:


#rearrage
df = df[['date','desc','debit_raw','credit_raw']]


# In[ ]:


#strip unneeded spaces
df.desc = df.desc.str.strip()
df.desc = df.desc.str.replace(" +"," ")


# In[ ]:


#export to csv
filename_csv_full = 'for import ' + filename.name
export_csv = df.to_csv (filename_csv_full, index = None, header=True)

