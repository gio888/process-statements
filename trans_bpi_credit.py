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
transactions_file=open(filename, "r")
contents =transactions_file.read()
transactions_file.close()


# In[ ]:


#make transformations
string = contents


# In[ ]:


#combine dates
pattern = r"(\w{3})(\n)"
replacement = r"\1 "
string1 = re.sub(pattern,replacement, string)


# In[ ]:


#get rid of PHP
pattern = "PHP "
replacement = r"\t"
string2 = re.sub(pattern,replacement, string1)


# In[ ]:


#get rid of commas
pattern = ","
replacement = ""
string3 = re.sub(pattern,replacement, string2)


# In[ ]:


#put year
pattern = r"(\w{3} \d{2})(\n)"
replacement = r"\1, 2020\t"
string4 = re.sub(pattern,replacement, string3)


# In[ ]:


#align amounts
pattern = r"(\n)(\t\d+\.\d{2})"
replacement = r"\2"
string5 = re.sub(pattern,replacement, string4)


# In[ ]:


#replace tabs with commas
pattern = r"\t"
replacement = r","
string6 = re.sub(pattern,replacement,string5)


# In[ ]:


#add headers
#string7 = "Date,TransID,Description,Amount,Balance\n" + string6
string7 = "date\tdescription\tamount\n" + string5


#print(string7)


# In[ ]:


#convert to dataframe

# wrap the string data in StringIO function 
StringData = StringIO(string7) 
  
# read the data using the Pandas read_csv() function 
df = pd.read_table(StringData)

#convert date column to mm/dd/yyy
df['date'] = pd.to_datetime(df.date)
df['date'] = df['date'].dt.strftime('%m/%d/%Y')


# In[ ]:


#lower
df.description = df.description.str.lower()


# In[ ]:


#create deposit and withdraw columns
df['withdraw'] = df['amount'].apply(lambda x: x if (x > 0) else 0)
df['deposit'] = df['amount'].apply(lambda x: -x if (x < 0) else 0)
#drop amount and balance columns
df.drop(['amount'], axis = 1, inplace = True)


# In[ ]:


df.head()


# In[ ]:


#export to csv
filename_csv_full = 'for import ' + filename.stem + ".csv"
df.to_csv (filename_csv_full, index = None, header=True)

