#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import libraries
import os
import pandas as pd
import re
import csv
from io import StringIO
from pathlib import Path


# In[2]:


#read file
filename = Path(input("Enter the file name : "))


# In[36]:


#load csv to dataframe
col_list = ['post_date', 'sale_date', 'desc', 'amount']
df = pd.read_csv(filename, names = col_list)


# In[37]:


#drop unneeded columns
df.drop(['post_date'], axis = 1, inplace = True)


# In[38]:


#fix date
#extract day month year
from datetime import datetime

day = df.sale_date.str.extract(r'(\d{2})', expand = False)
month = df.sale_date.str.extract(r'([A-Za-z]{3})', expand = False)
year = str(datetime.now().year)

# refill column
df['date'] = pd.to_datetime((month + ' ' + day + ', ' + year)).dt.strftime("%m/%d/%Y")


# In[39]:


#extract text from sale_date
df['desc01'] = df.sale_date.str.replace('\d{2} [A-Za-z]{3}','').str.strip()


# In[40]:


#get rid of nan rows
df = df.loc[-df.date.isna()]


# In[41]:


#fix desc
df['desc'] = df.desc.str.replace('\n',' ')


# In[42]:


df.desc = df.desc.fillna('')


# In[43]:


#combine descriptions
df['desc'] = df.desc01 + ' ' + df.desc


# In[44]:


#create deposit and withdraw columns
df['debit'] = df['amount'].apply(lambda x: x if ('CR'not in x) else '0')
df['credit'] = df['amount'].apply(lambda x: x if ('CR' in x) else '0').str.replace('CR','').fillna('0')


# In[45]:


#drop unneeded columns
df.drop(['sale_date','amount', 'desc01'], axis = 1, inplace = True)


# In[46]:


#set order
df = df[['date','desc','debit','credit']]


# In[47]:


#strip unneeded spaces
df.desc = df.desc.str.strip()
df.desc = df.desc.str.replace(" +"," ")


# In[48]:


#lower
df['desc'] = df.desc.str.lower()


# In[51]:


#replace spaces with decimal in dirty amounts
#(df.debit.str.isnumeric())
df.debit = df.debit.str.replace(' ','.')


# In[ ]:


#export to csv
filename_csv_full = 'for import ' + filename.name
export_csv = df.to_csv (filename_csv_full, index = None, header=True)

