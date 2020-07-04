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
df = pd.read_csv(filename,
                 usecols = [0,1,2],
                 names = ['date','desc','amount'])


# In[ ]:


#strip unneeded spaces
df['desc'] = df['desc'].str.strip()
df['desc'] = df['desc'].str.replace(" +"," ")


# In[ ]:


#convert to lower
df.desc = df.desc.str.lower()


# In[ ]:


#create deposit and withdraw columns
df['withdraw'] = df['amount'].apply(lambda x: -x if (x < 0) else 0)
df['deposit'] = df['amount'].apply(lambda x: x if (x > 0) else 0)
#drop amount and balance columns
df.drop(['amount'], axis = 1, inplace = True)


# In[ ]:


#export to csv
filename_csv_full = 'for import ' + filename.name
export_csv = df.to_csv (filename_csv_full, index = None, header=True)

