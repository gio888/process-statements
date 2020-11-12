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
col_list = ['date_raw', 'desc_raw', 'amount_raw']
df = pd.read_csv(filename, names = col_list)


# In[ ]:


#get rid of unneeded rows
df.date_raw = pd.to_datetime(df.date_raw, errors='coerce', dayfirst=True)
#df = df.loc[-df.date.isnull()]


# In[ ]:


#convert to default date format
df.date_raw = df.date_raw.dt.strftime('%m/%d/%Y')


# In[ ]:


#strip unneeded spaces
df.desc_raw = df.desc_raw.str.strip()
df.desc_raw = df.desc_raw.str.replace(" +"," ")


# In[ ]:


#lower
df['desc_raw'] = df.desc_raw.str.lower()


# In[ ]:


#create credit col from amount and clean it
df['credit'] = df.amount_raw.loc[df.amount_raw.str.contains(' -')]
df.credit = df.credit.str.replace(' -','')


# In[ ]:


#create debit col
df['debit'] = df.amount_raw.loc[~df.amount_raw.str.contains(' -')]


# In[ ]:


#get rid of nans
df.debit = df.debit.fillna(0)
df.credit = df.credit.fillna(0)


# In[ ]:


#drop amount_raw
df = df.drop(columns = 'amount_raw')


# In[ ]:


#rename columns
df.columns = ['date','desc','credit','debit']


# In[ ]:


#export to csv
filename_csv_full = 'for import ' + filename.name
export_csv = df.to_csv (filename_csv_full, index = None, header=True)

