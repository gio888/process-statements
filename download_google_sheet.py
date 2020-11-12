#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from googleapiclient.discovery import build
import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# In[ ]:


def gsheet_api_check(SCOPES):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


# In[ ]:


def pull_sheet_data(SCOPES,SPREADSHEET_ID,RANGE_NAME):
    creds = gsheet_api_check(SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME).execute()
    values = result.get('values', [])
    
    if not values:
        print('No data found.')
    else:
        rows = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                  range=RANGE_NAME).execute()
        data = rows.get('values')
        print("COMPLETE: Data copied")
        return data


# In[ ]:


def get_dict(html_content):
    from bs4 import BeautifulSoup
    from collections import defaultdict
    
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.table
    
    row_marker = 0
    details_dict = defaultdict(lambda: 'None')
    for row in table.find_all('tr'):
        column_marker = 0
        columns = row.find_all('td')
        if len(columns) > 1:
            for column in columns:
                if column_marker == 0:
                    x_key = column.get_text()
                else:
                    details_dict[x_key] = column.get_text()
                column_marker += 1
        row_marker += 1
    details_dict['Amount'] = float(details_dict['Amount'].replace('PHP ','').replace(',',''))
    return [details_dict['Amount'], details_dict['Notes']]


# In[ ]:


def get_amount(html_content):
    x_dict = get_dict(html_content)
    return x_dict[0]


# In[ ]:


def get_note(html_content):
    x_dict = get_dict(html_content)
    return x_dict[1]


# In[ ]:


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1Z5ajjyti3SiNMJz6AtleRiR-xJY-RGISqbRRUc5RLA0'
RANGE_NAME = 'Sheet1!A:B'
data = pull_sheet_data(SCOPES,SPREADSHEET_ID,RANGE_NAME)
df = pd.DataFrame(data[1:], columns=data[0])
df = df.drop(index = 0)


# In[ ]:


df['Amount'] = df.Body.apply(get_amount)
df['Note'] = df.Body.apply(get_note)


# In[ ]:


df = df.drop(columns = 'Body')


# In[ ]:


df.Date = df.Date.astype('datetime64[ns]')


# In[ ]:


from datetime import datetime
df['Date'] = df.Date.dt.strftime('%m-%d-%Y')


# In[ ]:


#export to csv
filename_csv_full = 'for import ' + 'bpi_check' + ".csv"
df.to_csv (filename_csv_full, index = None, header=True)

