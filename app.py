import streamlit as st
import pandas as pd
import numpy as np
import requests
#import psycopg2, psycopg2.extras


import yfinance as yf
from yahoo_fin.stock_info import get_data
import yahoo_fin.stock_info as si
from yahoo_fin import news
import time

import plotly.graph_objects as go
from plotly.subplots import make_subplots
#import streamlit.components.v1 as components

# tutorial https://www.youtube.com/watch?v=0ESc1bh3eIg&ab_channel=PartTimeLarry
# https://github.com/hackingthemarkets/streamlit-dashboards/blob/main/dashboard.py

#fetch from database
#connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)
#cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

#st.title("Financial Dashboard")

#st.header('This is a header')

#st.subheader('This is a subheader')

#st.write('this is regular text')

#some_dict  = {'key1':1,'key2':2}

#''' ============== Select Dashboard ============== '''
st.sidebar.title('Select Options')
option = st.sidebar.selectbox('Which Dashboard?', 
['chart','general','stocktwits'],0
#{'twitter','wallstreetbets','stocktwits','chart','pattern'}
)
#st.header(option)


#''' ============== Dashboards ============== '''
#if option == 'twitter':
    #st.subheader('twitter dashboard logic')

#https://algotrading101.com/learn/yahoo-finance-api-guide/
# http://theautomatic.net/yahoo_fin-documentation/#get_live_price
if option == 'chart':
    # https://towardsdatascience.com/free-stock-data-for-python-using-yahoo-finance-api-9dafd96cad2e
    st.header('Stock Chart Dashboard')
    
    symbol = st.sidebar.text_input('Stock Symbol',value='AAPL',max_chars=5,help='Enter Valid Stock Ticker Symbol')
    

    # get stock information from yahoo finance API
    stock = yf.Ticker(symbol)
    # get stock info
    #print(stock.info)
    st.subheader(symbol.upper()+' : '+stock.info['shortName'])

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    mkt_status = si.get_market_status()
    #st.markdown('Market Status = '+ str(mkt_status))
    col1.metric('Market Status',mkt_status)
    
    
    #st.markdown('Current Price = '+ str(round(live_price,2)))
    #while True:
        #live_price = si.get_live_price(symbol)
        #st.markdown('current price = '+ str(round(live_price,2)))
        #time.sleep(5) # Sleep for 5 seconds
        #print(live_price)

    period_name = st.sidebar.selectbox('Last Period', ['1 day', '5 day', 'yesterday', '1 month', '6 month', '1 year', '2 years', '5 years', '10 years', 'max'],index=4,help='select period of stock')
    interval = st.sidebar.selectbox('Interval', ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'],index=8,help='select time interval of stock')
    
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
    

    quote_data = si.get_quote_data(symbol)
    #print(quote_data)

    live_price = si.get_live_price(symbol)
    col2.metric('Current Market Price',round(live_price,2),delta=str(round(quote_data['regularMarketChange'],2))+' ('+str(round(quote_data['regularMarketChangePercent'],2))+'%)')

    if 'postMarketPrice' in quote_data:
        col3.metric('Post Market Price',round(quote_data['postMarketPrice'],2),delta=str(round(quote_data['postMarketChange'],2))+' ('+str(round(quote_data['postMarketChangePercent'],2))+'%)')

    if 'forwardPE' in quote_data:
        col4.metric('Forward P/E',str(round(quote_data['forwardPE'],2)))
    if 'priceToBook' in quote_data:
        col5.metric('Price to Book',str(round(quote_data['priceToBook'],2)))
    if 'averageAnalystRating' in quote_data:
        col6.metric('Analyst Rating - '+quote_data['averageAnalystRating'].split('-')[1],str(quote_data['averageAnalystRating'].split('-')[0]) + '/ 5.0',
                delta=None, delta_color="off")

    #components.html("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """)
    st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
    
    # get historical market 
    data = stock.history(period=period_dict[period_name],interval=interval)
    #data.index.apply()
    #data['percentage_change'] = data['Close']/data['Close'].shift(1)-1


    st.subheader(symbol.upper()+ ' Chart - Last '+period_name)
    #data = pd.read_sql()
    #st.dataframe(hist_df)  # Same as st.write(df)
    #data.columns.values[0]="date"
    #fig = make_subplots(rows=2, cols=1, row_heights=[1, 0.2], vertical_spacing=0.02,shared_xaxes=True) #row_heights=[1, 0.2], 
    fig = make_subplots(rows=2, cols=1, row_heights=[0.8, 0.2], 
                        vertical_spacing=0,shared_xaxes=True,
                        #row_heights=[1, 0.2], 
                        #subplot_titles=("First Subplot","Second Subplot")
    ) 

    #fig = go.Figure(data=[go.Candlestick(x=data.index,
                    #open=data['Open'],
                    #high=data['High'],
                    #low=data['Low'],
                    #close=data['Close'],
                    #name=symbol)]                 
                    #))
    fig.add_trace(go.Candlestick(x=data.index,open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'],
                             name=symbol), row=1, col=1)

    fig.add_trace(go.Scatter(x=data.index,y=data['Volume'], marker_color='#fae823', name='VOL', hovertemplate=[]), row=2, col=1)

    
    fig.update_layout({'plot_bgcolor': "#21201f", 'paper_bgcolor': "#21201f", 'legend_orientation': "h"},
                  legend=dict(y=1, x=0),
                  font=dict(color='#dedddc'), dragmode='pan', hovermode='x unified',
                  margin=dict(b=20, t=0, l=0, r=40))

    fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=True,
                 showspikes=True, spikemode='across', spikesnap='cursor', showline=False, spikedash='solid')

    #fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=True,
                 #showspikes=True, spikemode='across', spikesnap='cursor', showline=False, spikedash='solid')

    fig.update_xaxes(showgrid=False,type='category',zeroline=False,
    showspikes=True, spikemode='across', spikesnap='cursor', showline=False, spikedash='solid' )

    fig.update_layout(title=symbol.upper()+' Price - '+period_name,
                    yaxis_title='Price',
                    #xaxis_title='Date',
                    xaxis_rangeslider_visible=False,
                    height=700) #xaxis_rangeslider_visible=False
              
    #fig.update_xaxes(title_font=dict(size=18, family='Courier', color='crimson'))
    #fig.update_yaxes(title_font=dict(size=18, family='Courier', color='crimson'))
    #fig.update_layout(hoverdistance=0)
    #fig.update_traces(xaxis='x')
    st.plotly_chart(fig, use_container_width=True)

    #fig.update_layout(yaxis_title=symbol.upper()+' Price (USD)',
    #xaxis_title='Date',
        #height=700) #xaxis_rangeslider_visible=False

    data['MA50'] = data['Open'].rolling(50).mean()
    data['MA200'] = data['Open'].rolling(200).mean()
    
    st.line_chart(data=data[['Close','Open','MA50','MA200']],use_container_width=True)

    # show dataframe
    #st.subheader('Stock Dataframe')
    #st.write(data)

    st.image(f"https://finviz.com/chart.ashx?t={symbol}",caption=symbol+' stock chart retrieved from finviz')
    
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

    #st.write(stock_news)


if option == 'general':
    st.subheader('General Dashboard')
    #symbol = st.sidebar.text_input('Stock Symbol',value='AAPL',max_chars=5)
    st.subheader('Table of the top 100 undervalued large caps')
    large_cap_table = si.get_undervalued_large_caps()
    st.write(large_cap_table)

    #symbol = st.sidebar.text_input('Stock Symbol',value='AAPL',max_chars=5)
    

#if option == 'wallstreetbets':
    #st.subheader('wallstreetbets dashboard logic')

if option == 'stocktwits':
    #st.subheader('chart dashboard logic')
    #symbol= 'AAPL'
    
    symbol = st.sidebar.text_input('Stock Symbol',value='AAPL',max_chars=5,help='Enter Valid Stock Ticker Symbol')
    st.subheader('Stockwits - '+symbol)
    st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
    r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json")
    data = r.json()

    for message in data['messages']:
        st.image(message['user']['avatar_url'])
        st.write(message['user']['username'])
        st.write(message['created_at'])
        st.write(message['body'])
        st.write('_______________________________________________________________')

    #st.write(data)

st.sidebar.write('Made by Ng Zhili - 2021')
st.sidebar.write("View source code [here](https://github.com/ngzhili/financial-dashboard)")

#df = pd.DataFrame(
    #np.random.randn(50, 20),
    #columns=('col %d' % i for i in range(20)))

#st.dataframe(df)  # Same as st.write(df)

#st.image('https://www.nasdaq.com/sites/acquia.prod/files/styles/720x400/public/image/fad5aa82561887202560b4dba338bef2a56751e6_742299cbdba5f731f487c3c190f8cee5.png?itok=BuSFq0hp')