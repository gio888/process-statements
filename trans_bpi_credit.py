#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import libraries
import os
import pandas as pd
import re
import csv
from io import StringIO


# In[2]:


#read file
filename = input("Enter the file name : ")
full_filename = filename + ".txt"
transactions_file=open(full_filename, "r")
contents =transactions_file.read()
transactions_file.close()


# In[3]:


#make transformations
string = contents
#print(string)


# In[4]:


#combine dates
pattern = r"(\w{3})(\n)"
replacement = r"\1 "
string1 = re.sub(pattern,replacement, string)

#print(string1)


# In[ ]:


#combine description
#pattern = r"(\d{2})(\n)(\d{2,4})"
#replacement = r"\1\t\3"
#string2 = re.sub(pattern,replacement, string1)

#print(string2)


# In[ ]:


#combine amount and balance
#pattern = r"(\.\d{2})(\n)(PHP )"
#replacement = r"\1\t"
#string3 = re.sub(pattern,replacement, string2)

#print(string3)


# In[5]:


#get rid of PHP
pattern = "PHP "
replacement = r"\t"
string2 = re.sub(pattern,replacement, string1)

#print(string2)


# In[ ]:


#separate transaction number
#pattern = r"(\t)(\d{4})( )"
#replacement = r"\1\2\t"
#string5 = re.sub(pattern,replacement, string4)

#print(string5)


# In[6]:


#get rid of commas
pattern = ","
replacement = ""
string3 = re.sub(pattern,replacement, string2)

#print(string3)


# In[7]:


#put year
pattern = r"(\w{3} \d{2})(\n)"
replacement = r"\1, 2020\t"
string4 = re.sub(pattern,replacement, string3)

#print(string4)


# In[16]:


#align amounts
pattern = r"(\n)(\t\d+\.\d{2})"
replacement = r"\2"
string5 = re.sub(pattern,replacement, string4)

#print(string5)


# In[17]:


#replace tabs with commas
pattern = r"\t"
replacement = r","
string6 = re.sub(pattern,replacement,string5)

#print(string6)


# In[19]:


# wrap the string data in StringIO function 
#StringData = StringIO(string6) 
  
# read the data using the Pandas read_csv() function 
#df = pd.read_csv(StringData, names = ['date','description','amount'])
#df.head()


# In[30]:


#add headers
#string7 = "Date,TransID,Description,Amount,Balance\n" + string6
string7 = "date\tdescription\tamount\n" + string5


#print(string7)


# In[31]:


#convert to dataframe

# wrap the string data in StringIO function 
StringData = StringIO(string7) 
  
# read the data using the Pandas read_csv() function 
df = pd.read_table(StringData)

#convert date column to mm/dd/yyy
df['date'] = pd.to_datetime(df.date)
df['date'] = df['date'].dt.strftime('%m/%d/%Y')


# In[32]:


#df.head()


# In[33]:


#lower
df.description = df.description.str.lower()
#df.head()


# In[ ]:


#export to csv
current_dir = os.getcwd()
filename_csv_full = current_dir + "/" + filename + ".csv"
export_csv = df.to_csv (filename_csv_full, index = None, header=True)


# In[ ]:




