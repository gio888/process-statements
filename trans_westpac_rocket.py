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
col_list = ['date', 'desc', 'debit', 'credit']
df = pd.read_csv(filename, usecols = [0,1,2,3], names = col_list)


# In[ ]:


#get rid of unneeded rows
df.date = pd.to_datetime(df.date, errors='coerce', dayfirst=False)
df = df.loc[-df.date.isnull()]


# In[ ]:


#convert to default date format
df.date = df.date.dt.strftime('%m/%d/%Y')


# In[ ]:


#fix desc
df['desc'] = df.desc.str.replace('\n',' ')


# In[ ]:


#strip unneeded spaces
df.desc = df.desc.str.strip()
df.desc = df.desc.str.replace(" +"," ")


# In[ ]:


#lower
df['desc'] = df.desc.str.lower()


# In[ ]:


#get rid of nans
df.debit = df.debit.fillna(0)
df.credit = df.credit.fillna(0)


# In[ ]:


df = df.loc[-((df.debit == 0) & (df.credit == 0)),:]


# In[ ]:


#export to csv
filename_csv_full = 'for import ' + filename.name
export_csv = df.to_csv (filename_csv_full, index = None, header=True)

