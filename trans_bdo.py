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


#read the csv file
header_list = ['Posting Date','Description','Blank1','Branch','Debit Amount',
          'Blank2','Credit Amount','Blank3','Running Balance','Blank4',
          'Currency','Check Number']
df = pd.read_csv(filename, names = header_list)
#df.head(30)


# In[ ]:


#drop unneeded rows

#drop top rows
df = df.iloc[6:]

#drop last 2 rows
df = df.iloc[:-2]
df = df.reset_index(drop=True)


# In[ ]:


#drop unneeded columns

df = df.drop(columns = ['Blank1','Blank2','Blank3','Running Balance','Blank4','Currency','Check Number'])


# In[ ]:


#get rid of commas
df['Debit Amount'] = df['Debit Amount'].str.replace(',', '')
df['Credit Amount'] = df['Credit Amount'].str.replace(',', '')


# In[ ]:


#get rid of NaNs
df = df.fillna(value = 0)


# In[ ]:


#convert date to datetime
df['Posting Date'] = pd.to_datetime(df['Posting Date'])
df['Posting Date'] = df['Posting Date'].dt.strftime('%m/%d/%Y')


# In[ ]:


#combine description and branch
df['Description'] = df['Description'] + ' ' + df['Branch']


# In[ ]:


#strip unneeded spaces
df['Description'] = df['Description'].str.strip()
df['Description'] = df['Description'].str.replace(" +"," ")


# In[ ]:


#lower case
df['Description'] = df['Description'].str.lower()


# In[ ]:


#drop branch columns
df = df.drop(columns = 'Branch')


# In[ ]:


#export to csv
filename_csv_full = 'for import ' + filename.stem + ".csv"
df.to_csv (filename_csv_full, index = None, header=True)

