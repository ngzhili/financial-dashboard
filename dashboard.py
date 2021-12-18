import streamlit as st
import pandas as pd
import numpy as np
import requests
import psycopg2, psycopg2.extras
import plotly.graph_objects as go

# tutorial https://www.youtube.com/watch?v=0ESc1bh3eIg&ab_channel=PartTimeLarry
# https://github.com/hackingthemarkets/streamlit-dashboards/blob/main/dashboard.py

#fetch from database
#connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)
#cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

#st.title("Finanial Dashboard")

#st.header('This is a header')

#st.subheader('This is a subheader')

#st.write('this is regular text')

#some_dict  = {'key1':1,'key2':2}


import yfinance as yf



#''' ============== Select Dashboard ============== '''
st.sidebar.title('Options')
option = st.sidebar.selectbox('Which Dashboard?', 
{'wallstreetbets','stocktwits','chart','pattern'},1
#{'twitter','wallstreetbets','stocktwits','chart','pattern'}
)
#st.header(option)


#''' ============== Dashboards ============== '''
#if option == 'twitter':
    #st.subheader('twitter dashboard logic')

import plotly.graph_objects as go

if option == 'chart':
    # https://towardsdatascience.com/free-stock-data-for-python-using-yahoo-finance-api-9dafd96cad2e
    st.subheader('Stock Chart Dashboard')
    symbol = st.sidebar.text_input('Stock Symbol',value='AAPL',max_chars=5)
    period_name = st.sidebar.selectbox('Period', ['1 day', '5 day', 'yesterday', '1 month', '6 month', '1 year', '2 years', '5 years', '10 years', 'max'],index=4,help='select period of stock')
    interval = st.sidebar.selectbox('Period', ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'],index=8,help='select time interval of stock')

    period_dict = {'1 day':'1d', 
    '5 day':'5d', 
    'yesterday':'ytd', 
    '1 month':'1mo', 
    '3 month':'3mo', 
    '6 month':'6mo', 
    '1 year':'1y', 
    '2 years':'2y', 
    '5 years':'5y', 
    '10 years':'10y', 
    'max':'max'}

    # get stock information from yahoo finance API
    stock = yf.Ticker(symbol)
    # get stock info
    #print(msft.info)

    # get historical market 
    data = stock.history(period=period_dict[period_name])
    #data = pd.read_sql()
    #st.dataframe(hist_df)  # Same as st.write(df)
    st.subheader(symbol.upper())
    fig = go.Figure(data=[go.Candlestick(x=data.iloc[:,0],
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                    name=symbol)]                 
                    )
    fig.update_xaxes(type='category')
    fig.update_layout(height=700)
    st.plotly_chart(fig, use_container_width=True)
    st.write(data)



if option == 'pattern':
    st.subheader('Pattern Chart Dashboard')
    symbol = st.sidebar.text_input('Stock Symbol',value='AAPL',max_chars=5)

    st.image(f"https://finviz.com/chart.ashx?t={symbol}")

#if option == 'wallstreetbets':
    #st.subheader('wallstreetbets dashboard logic')

if option == 'stocktwits':
    #st.subheader('chart dashboard logic')
    #symbol= 'AAPL'
    symbol = st.sidebar.text_input('Stock Symbol',value='AAPL',max_chars=5)

    r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json")
    data = r.json()

    for message in data['messages']:
        st.image(message['user']['avatar_url'])
        st.write(message['user']['username'])
        st.write(message['created_at'])
        st.write(message['body'])

    st.write(data)



#df = pd.DataFrame(
    #np.random.randn(50, 20),
    #columns=('col %d' % i for i in range(20)))

#st.dataframe(df)  # Same as st.write(df)

#st.image('https://www.nasdaq.com/sites/acquia.prod/files/styles/720x400/public/image/fad5aa82561887202560b4dba338bef2a56751e6_742299cbdba5f731f487c3c190f8cee5.png?itok=BuSFq0hp')