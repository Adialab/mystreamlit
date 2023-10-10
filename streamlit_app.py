import time

import streamlit as st

import numpy as np
import pandas as pd

st.title('我的第一個應用程式')

st.write("嘗試創建**表格**：")

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})
df

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])
st.line_chart(chart_data)

map_data = pd.DataFrame(
    np.random.randn(100, 2) / [50, 50] + [23.9738835,120.9791046],
    columns=['lat', 'lon'],
    zoom=3)
st.map(map_data)

