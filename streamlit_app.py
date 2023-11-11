import time

import streamlit as st
import numpy as np
import pandas as pd
import requests
from io import StringIO
import json
import re

CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

def crawlerStock(date):
    data = requests.get('https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX?date='+date+'&type=ALLBUT0999&response=json').text
    data = cleanhtml(data)
    json_data = json.loads(data)
    pre_data = json_data['tables'][8]['data']
    
    stock_data = pd.DataFrame(pre_data, columns = ['stock_id', 'Stock_name', 'traded_volumn', 'traded_lots', 'traded_cash', 'open', 'high','low','close', 'change','change_in_price','last_revealed_buy_price','last_revealed_buy_volume','last_revealed_sell_price','last_revealed_sell_volume','pe_ratio'])
    stock_data.insert(len(stock_data.columns), 'date', date)
    stock_data['date'] = pd.to_datetime(stock_data['date'].astype(str))
    stock_data['traded_volumn'] = stock_data['traded_volumn'].str.replace(',','').astype(int)
    stock_data['traded_lots'] = stock_data['traded_lots'].str.replace(',','').astype(int)
    stock_data['traded_cash'] = stock_data['traded_cash'].str.replace(',','').astype(int)
    #stock_data = stock_data.astype({'open':'float','high':'float','low':'float','close':'float'})
    return stock_data

st.title('我的第一個Streamlit應用程式')

st.write("嘗試創建**表格**：")
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 30, 40, 20]
})
st.dataframe(df.style.highlight_max(axis=0))

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])
st.line_chart(chart_data)

date_input = st.text_input("Enter some date , ex. 20231013 👇")
if date_input:
    date = date_input
    try:
        StockData = crawlerStock(date)
        edited_df = st.data_editor(StockData)
    except:
        print('Something Error...')
        pass

if st.sidebar.checkbox('顯示地圖'):
    map_data = pd.DataFrame(
        np.random.randn(200, 2) / [50, 50] + [23.9738835,120.9791046],
        columns=['lat', 'lon'])
    st.map(map_data, zoom=6)

if st.sidebar.checkbox('播放影片'):
    st.video("https://youtu.be/zQwz5CAGSY0")

if st.sidebar.checkbox('日出沒時刻'):
    cwa_json_data  = requests.get('https://opendata.cwa.gov.tw/api/v1/rest/datastore/A-B0062-001?Authorization=CWA-D1D952FD-2A6B-459F-9127-7CAE3C6B04FE')
    cwa_data = pd.read_json(cwa_json_data, convert_dates=True)
    st.json(cwa_data)


