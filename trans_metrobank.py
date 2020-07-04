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
df = pd.read_csv(filename,skiprows = 4, usecols = [0,1,3,4])


# In[ ]:


#strip unneeded spaces
df['Description'] = df['Description'].str.strip()
df['Description'] = df['Description'].str.replace(" +"," ")


# In[ ]:


#convert to lower
df.Description = df.Description.str.lower()


# In[ ]:


#export to csv
filename_csv_full = 'for import ' + filename.name
export_csv = df.to_csv (filename_csv_full, index = None, header=True)

