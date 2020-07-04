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
df = pd.read_csv(filename, names = ['datetime','desc','id','withdraw','deposit'], usecols = [0,1,2,3,4])[:-3]


# In[ ]:


#convert id to integer then to a string
df['id'] = df['id'].astype('int64')
df['id'] = df['id'].astype('str')


# In[ ]:


#join desc + id then drop it
df['desc'] = df['desc'] + ' ' + df['id']
df.drop(columns = ['id'],inplace = True)


# In[ ]:


df['datetime'] = pd.to_datetime(df['datetime'])
df['datetime'] = df['datetime'].dt.strftime('%m/%d/%Y')


# In[ ]:


#get rid of NaNs
df = df.fillna(value = 0)


# In[ ]:


#lower case
df['desc'] = df['desc'].str.lower()


# In[ ]:


#strip unneeded spaces
df['desc'] = df['desc'].str.strip()
df['desc'] = df['desc'].str.replace(" +"," ")


# In[ ]:


#change order
df = df[['datetime','desc','deposit','withdraw']]


# In[ ]:


#export to csv
filename_csv_full = 'for import ' + filename.name
export_csv = df.to_csv (filename_csv_full, index = None, header=True)

