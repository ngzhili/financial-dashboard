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
#from yahoo_fin.stock_info import get_data

from yahoo_fin.stock_info import get_data
import yahoo_fin.stock_info as si

#''' ============== Select Dashboard ============== '''
st.sidebar.title('Options')
option = st.sidebar.selectbox('Which Dashboard?', 
{'wallstreetbets','stocktwits','chart','pattern','general'},1
#{'twitter','wallstreetbets','stocktwits','chart','pattern'}
)
#st.header(option)


#''' ============== Dashboards ============== '''
#if option == 'twitter':
    #st.subheader('twitter dashboard logic')

import plotly.graph_objects as go
import time

#https://algotrading101.com/learn/yahoo-finance-api-guide/
# http://theautomatic.net/yahoo_fin-documentation/#get_live_price
if option == 'chart':
    # https://towardsdatascience.com/free-stock-data-for-python-using-yahoo-finance-api-9dafd96cad2e
    st.subheader('Stock Chart Dashboard')

    symbol = st.sidebar.text_input('Stock Symbol',value='AAPL',max_chars=5)

    # get stock information from yahoo finance API
    stock = yf.Ticker(symbol)
    # get stock info
    #print(stock.info)


    st.subheader(symbol.upper()+' : '+stock.info['shortName'])
    
    period_name = st.sidebar.selectbox('Last Period', ['1 day', '5 day', 'yesterday', '1 month', '6 month', '1 year', '2 years', '5 years', '10 years', 'max'],index=4,help='select period of stock')
    interval = st.sidebar.selectbox('Interval', ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'],index=8,help='select time interval of stock')


    col1, col2, col3 = st.columns(3)
    mkt_status = si.get_market_status()
    #st.markdown('Market Status = '+ str(mkt_status))
    col1.metric('Market Status',mkt_status)
    
    live_price = si.get_live_price(symbol)
    col2.metric('Current Price',round(live_price,2),delta="percentage change %")
    #st.markdown('Current Price = '+ str(round(live_price,2)))
    #while True:
        #live_price = si.get_live_price(symbol)
        #st.markdown('current price = '+ str(round(live_price,2)))
        #time.sleep(5) # Sleep for 5 seconds
        #print(live_price)

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

   

    # get historical market 
    data = stock.history(period=period_dict[period_name])
    #data = pd.read_sql()
    #st.dataframe(hist_df)  # Same as st.write(df)
    

    fig = go.Figure(data=[go.Candlestick(x=data.iloc[:,0],
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                    name=symbol)]                 
                    )
    fig.update_xaxes(type='category')
    fig.update_layout(yaxis_title=symbol.upper()+' Price',
    xaxis_title='Date',
        height=700) #xaxis_rangeslider_visible=False

    fig.update_xaxes(title_font=dict(size=18, family='Courier', color='crimson'))
    fig.update_yaxes(title_font=dict(size=18, family='Courier', color='crimson'))
    st.plotly_chart(fig, use_container_width=True)

    fig.update_layout(yaxis_title=symbol.upper()+' Price (USD)',xaxis_title='Date',
        height=700) #xaxis_rangeslider_visible=False
    st.line_chart(data=data[['Close','Open']],width=0, height=0, use_container_width=True)

    st.write(data)

from yahoo_fin import news
if option == 'general':
    st.subheader('General Dashboard')
    #symbol = st.sidebar.text_input('Stock Symbol',value='AAPL',max_chars=5)
    st.subheader('Table of the top 100 undervalued large caps')
    large_cap_table = si.get_undervalued_large_caps()
    st.write(large_cap_table)

    symbol = st.sidebar.text_input('Stock Symbol',value='AAPL',max_chars=5)
    
    st.subheader('Yearly Income Statement of '+ str(symbol))
    # get yearly data
    income_statement_yearly = si.get_income_statement(symbol)
    st.write(income_statement_yearly)

    st.subheader('Quarterly Income Statement of '+ str(symbol))
    # get quarterly data
    income_statement_quarterly = si.get_income_statement(symbol, yearly = False)
    st.write(income_statement_quarterly)
    
    st.subheader('Yahoo Finance News of '+ str(symbol))
    stock_news = news.get_yf_rss(symbol)

    count = 1 
    for message in stock_news:
        st.write(str(count)+'. '+message['title'])
        st.write('Published '+message['published'])
        st.write(message['summary'])
        st.write('_______________________________________________________________')

        count+=1

    st.write(stock_news)

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
    st.subheader('Stockwits - '+symbol)
    r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json")
    data = r.json()

    for message in data['messages']:
        st.image(message['user']['avatar_url'])
        st.write(message['user']['username'])
        st.write(message['created_at'])
        st.write(message['body'])
        st.write('_______________________________________________________________')

    st.write(data)



#df = pd.DataFrame(
    #np.random.randn(50, 20),
    #columns=('col %d' % i for i in range(20)))

#st.dataframe(df)  # Same as st.write(df)

#st.image('https://www.nasdaq.com/sites/acquia.prod/files/styles/720x400/public/image/fad5aa82561887202560b4dba338bef2a56751e6_742299cbdba5f731f487c3c190f8cee5.png?itok=BuSFq0hp')