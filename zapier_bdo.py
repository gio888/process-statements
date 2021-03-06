# -*- coding: utf-8 -*-
"""zapier_bdo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12VbxSRwhY9p1yEMfPViZ5e38gZsPNPSo
"""

from google.colab import auth
auth.authenticate_user()
import gspread
from oauth2client.client import GoogleCredentials
gc = gspread.authorize(GoogleCredentials.get_application_default())

import pandas as pd

wb = gc.open_by_url('https://docs.google.com/spreadsheets/d/16C2iXhN-Xmh0xZa__xxDIhi_QFj55wgFEWgCsLXEc7c/edit#gid=0')

sheet = wb.worksheet('Sheet1')

data = sheet.get_all_values()

df = pd.DataFrame(data)
df.columns = df.iloc[0]
df = df.iloc[1:]

df_schema = {
    'Date': df['Date'].astype('datetime64'), 
    'Description': df['Description'].astype(str), 
    }

df = pd.DataFrame(df_schema)

df['destination_account'] = df.Description.str.extract(r'(Destination Account: .+)',expand = False).str.replace('Destination Account: ','').str.replace('\r','')

df['ref_num'] = df.Description.str.extract(r'(Reference Number: .+\.)',expand = False).str.replace('Reference Number: ','').str.replace('\.','')

df['amount'] = df.Description.str.extract(r'(Transaction Amount: PHP .+)',expand = False).str.replace('Transaction Amount: PHP ','').str.replace('\r','').str.replace(',','')

df['amount'] = df.amount.astype('float')

df['memo'] = df.Description.str.extract(r'(Message to Beneficiary: .+)',expand = False).str.replace('Message to Beneficiary: ','').str.replace('\r','').str.lower()

df['date'] = df.Date.dt.date

df0 = df.copy()

df = df[['date', 'memo', 'amount', 'destination_account', 'ref_num']]