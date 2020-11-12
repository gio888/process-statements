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
col_list = ['Date', 'Description', 'Debit', 'Credit', 'Balance']
df = pd.read_csv(filename, names = col_list)


# In[ ]:


#lowercase
#for cols in col_list:
#    df[cols] = df[cols].str.lower()

df.Description = df.Description.str.lower()


# In[ ]:


#strip unneeded spaces
df['Description'] = df['Description'].str.strip()
df['Description'] = df['Description'].str.replace(" +"," ")


# In[ ]:


#get rid of NaNs
df = df.fillna(value = 0)


# In[ ]:


#drop balance columns
df.drop(['Balance'], axis = 1, inplace = True)


# In[ ]:


#export to csv
filename_csv_full = 'for import ' + filename.name
export_csv = df.to_csv (filename_csv_full, index = None, header=True)

