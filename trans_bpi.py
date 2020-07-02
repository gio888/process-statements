#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import libraries
import os
import pandas as pd
import re
import csv
from io import StringIO


# In[ ]:


#read file
currentDirectory = os.getcwd()
filename = input("Enter the file name : ")
full_filename = currentDirectory + "/" + filename + ".txt"
transactions_file=open(full_filename, "r")
contents =transactions_file.read()
transactions_file.close()


# In[ ]:


#make transformations
string = contents
#print(string)


# In[ ]:


#make everything 1 long string
#months = [Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec]
pattern = r"\n"
replacement = " "
string01 = re.sub(pattern,replacement, string)

#print(string01)


# In[ ]:


#separate by date
pattern = r"( Jan| Feb| Mar| Apr| May| Jun| Jul| Aug| Sep| Oct| Nov| Dec)"
replacement = r"\n\1"
string02 = re.sub(pattern,replacement, string01)

#print(string02)


# In[ ]:


#get rid of extra spaces
pattern = r"\n "
replacement = r"\n"
string03 = re.sub(pattern,replacement, string02)

#print(string03)


# In[ ]:


#get rid of commas
pattern = ","
replacement = ""
string04 = re.sub(pattern,replacement, string03)

#print(string04)


# In[ ]:


#separate date
pattern = r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)( \d{2})( )"
replacement = r"\1\2,"
string05 = re.sub(pattern,replacement, string04)

#print(string05)


# In[ ]:


#get rid of PHP
pattern = " PHP "
replacement = ","
string06 = re.sub(pattern,replacement, string05)

#print(string06)


# In[ ]:


#add headers
string07 = "Date,Description,Amount,Balance\n" + string06


#print(string07)


# In[ ]:


#convert to dataframe

# wrap the string data in StringIO function 
StringData = StringIO(string07) 
  
# read the data using the Pandas read_csv() function 
df = pd.read_csv(StringData,parse_dates=[1],infer_datetime_format=True)
df.dtypes

#convert date column to mm/dd/yyy
df['Date'] = pd.to_datetime(df.Date + r", 2020")
df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')


# In[ ]:


#convert to lower
df.Description = df.Description.str.lower()


# In[ ]:


#create deposit and withdraw columns
df['Deposit'] = df['Amount'].apply(lambda x: x if (x > 0) else 0)
df['Withdraw'] = df['Amount'].apply(lambda x: -x if (x < 0) else 0)


# In[ ]:


#drop amount and balance columns
df.drop(['Amount','Balance'], axis = 1, inplace = True)


# In[ ]:


#export to csv
#current_dir = os.getcwd()
#filename_csv_full = current_dir + "/" + filename + ".csv"
filename_csv_full = filename + ".csv"
export_csv = df.to_csv (filename_csv_full, index = None, header=True)

