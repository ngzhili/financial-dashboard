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
#from numerize import numerize
# tutorial https://www.youtube.com/watch?v=0ESc1bh3eIg&ab_channel=PartTimeLarry
# https://github.com/hackingthemarkets/streamlit-dashboards/blob/main/dashboard.py

#fetch from database
#connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)
#cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])

#''' ============== Select Dashboard ============== '''
st.sidebar.title('Select Options')
option = st.sidebar.selectbox('Which Dashboard?', 
['chart','general','stocktwits'],1
#{'twitter','wallstreetbets','stocktwits','chart','pattern'}
)
#st.header(option)

# ''' ===== Get All Stock Tickers for US Stocks ===== '''

# gather stock symbols from major US exchanges
df1 = pd.DataFrame( si.tickers_sp500() )
df2 = pd.DataFrame( si.tickers_nasdaq() )
df3 = pd.DataFrame( si.tickers_dow() )
df4 = pd.DataFrame( si.tickers_other() )

# convert DataFrame to list, then to sets
sym1 = set( symbol for symbol in df1[0].values.tolist() )
sym2 = set( symbol for symbol in df2[0].values.tolist() )
sym3 = set( symbol for symbol in df3[0].values.tolist() )
sym4 = set( symbol for symbol in df4[0].values.tolist() )

# join the 4 sets into one. Because it's a set, there will be no duplicate symbols
symbols = set.union( sym1, sym2, sym3, sym4 )

# Some stocks are 5 characters. Those stocks with the suffixes listed below are not of interest.
my_list = ['W', 'R', 'P', 'Q']

# W means there are outstanding warrants. We don’t want those.
# R means there is some kind of “rights” issue. Again, not wanted.
# P means “First Preferred Issue”. Preferred stocks are a separate entity.
# Q means bankruptcy. We don’t want those, either.

#del_set = set()
sav_set = set()

for symbol in symbols:
    if len( symbol ) > 4 and symbol[-1] in my_list or "$" in symbol:
        pass
        #del_set.add( symbol )
    else:
        sav_set.add( symbol )

sav_set = sorted(sav_set)
#print(symbols)        

#print( f'Removed {len( del_set )} unqualified stock symbols...' )
#print( f'There are {len( sav_set )} qualified stock symbols...' )


#''' ============== Dashboards ============== '''
#if option == 'twitter':
    #st.subheader('twitter dashboard logic')

#https://algotrading101.com/learn/yahoo-finance-api-guide/
# http://theautomatic.net/yahoo_fin-documentation/#get_live_price
if option == 'chart':
    # https://towardsdatascience.com/free-stock-data-for-python-using-yahoo-finance-api-9dafd96cad2e
    symbol = st.sidebar.selectbox('Stock Symbol', sav_set,index=50,help='Enter Valid Stock Ticker Symbol')

    #symbol = st.sidebar.text_input('Stock Symbol',value='AAPL',max_chars=5,help='Enter Valid Stock Ticker Symbol')
    st.header('Stock Chart Dashboard - '+symbol)
    st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
    # get stock information from yahoo finance API
    stock = yf.Ticker(symbol)
    # print(stock)
    # get stock info
    # print(stock.info)
    try: 
        st.subheader(symbol.upper()+' : '+stock.info['shortName'])
    except:
        st.subheader(symbol.upper())
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    col7, col8, col9 = st.columns(3)
    mkt_status = si.get_market_status()
    #st.markdown('Market Status = '+ str(mkt_status))
    col1.metric('Market Status',mkt_status)
    
    #st.markdown('Current Price = '+ str(round(live_price,2)))
    #while True:
        #live_price = si.get_live_price(symbol)
        #st.markdown('current price = '+ str(round(live_price,2)))
        #time.sleep(5) # Sleep for 5 seconds
        #print(live_price)

    period_name = st.sidebar.selectbox('Last Period', ['yesterday','1 day', '5 day', '1 month', '3 months','6 months', '1 year', '2 years', '5 years', '10 years', 'max'],index=5,help='select period of stock')
    
    interval_list = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
    interval_dict = {'yesterday':(0,9), 
                    '1 day':(0,9), 
                    '5 day':(0,10), 
                    '1 month':(1,12), 
                    '3 months':(7,13), 
                    '6 months':(7,13), 
                    '1 year':(7,13), 
                    '2 years':(7,13), 
                    '5 years':(8,13), 
                    '10 years':(8,13), 
                    'max':(8,13)
                    }
    
    interval = st.sidebar.selectbox('Interval', interval_list[interval_dict[period_name][0]:interval_dict[period_name][1]],index=1,help='select time interval of stock')
    
    period_dict = {'1 day':'1d', 
    '5 day':'5d', 
    'yesterday':'ytd', 
    '1 month':'1mo', 
    '3 months':'3mo', 
    '6 months':'6mo', 
    '1 year':'1y', 
    '2 years':'2y', 
    '5 years':'5y', 
    '10 years':'10y', 
    'max':'max'}

    #text_length = st.slider("Choose text length", value=[1,3], step=1)
    #full_text = 'abcdefghij'
    #output_text = full_text[:text_length]
    #st.markdown(output_text)   
    quote_data = si.get_quote_data(symbol)
    quote_table = si.get_quote_table(symbol)
    #print(quote_table)
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

    if 'marketCap' in quote_data:
        mkt_cap_value = quote_data['marketCap']
        #print(numerize.numerize(100003230230000000000))
        #print(type(mkt_cap_value))
        #1234567.12)
        col7.metric('Market Cap',str(human_format(mkt_cap_value)),
                delta=None, delta_color="off")

    if 'EPS (TTM)' in quote_table:
        col8.metric('EPS (TTM)',quote_table['EPS (TTM)'],
                delta=None, delta_color="off")
    if 'Forward Dividend & Yield' in quote_table:
        col9.metric('Forward Dividend & Yield',quote_table['Forward Dividend & Yield'],
                delta=None, delta_color="off")
        
    #components.html("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """)
    st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
    
    # get historical market 
    data = stock.history(period=period_dict[period_name],interval=interval)
    #data.index.apply()
    #data['percentage_change'] = data['Close']/data['Close'].shift(1)-1


    st.subheader(symbol.upper()+ ' Chart - '+period_name)
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
    try:
        
        # get yearly income statement data
        income_statement_yearly = si.get_income_statement(symbol)
        st.subheader('Yearly Income Statement of '+ str(symbol))
        st.write(income_statement_yearly)

        
        # get quarterly income statement data
        income_statement_quarterly = si.get_income_statement(symbol, yearly = False)
        st.subheader('Quarterly Income Statement of '+ str(symbol))
        st.write(income_statement_quarterly)


        cashflow = si.get_cash_flow(symbol)
        st.subheader('Cash Flow Statement of '+ str(symbol))
        st.write(cashflow)


    except:
        pass

    try:
        st.subheader('Yahoo Finance News of '+ str(symbol))
        stock_news = news.get_yf_rss(symbol)
        st.write('Displaying '+str(len(stock_news))+f' most recent yahoo finance news of {symbol}.')

        st.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
        count = 1 
        for message in stock_news:
            st.write(str(count)+'. '+message['title'])
            st.write('Published '+message['published'])
            st.write(message['summary'])
            #st.write('_______________________________________________________________')
            st.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
            count+=1
    except:
        pass
    #st.write(stock_news)
    # except:
    #     st.error('Please enter a valid stock ticker')



if option == 'general':
    st.header('General Dashboard')
    st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
    #symbol = st.sidebar.text_input('Stock Symbol',value='AAPL',max_chars=5)
    st.subheader('Table of the top 100 undervalued large caps')
    large_cap_table = si.get_undervalued_large_caps()
    st.write(large_cap_table)

    st.subheader('Table of S&P 500')
    tickers = si.tickers_sp500(include_company_data = True)
    st.write(tickers)

    st.subheader('Table of Nasdaq')
    tickers = si.tickers_nasdaq(include_company_data = True)
    st.write(tickers)

    st.subheader('Table of Dow Jones')
    tickers = si.tickers_dow(include_company_data = True)
    st.write(tickers)

    st.subheader('Table of FTSE 100 Index')
    tickers = si.tickers_ftse100(include_company_data = True)
    st.write(tickers)

    # st.subheader('Table of top 100 cryptocurrencies by market cap')
    	
    # table_crypto = si.get_top_crypto()
    # #for i in table_crypto:
    #     #print(i)
    # st.write(table_crypto[['Symbol',
    #         'Name',
    #         'Price (Intraday)',
    #         'Change',
    #         '% Change',
    #         'Market Cap',
    #         'Volume in Currency (Since 0:00 UTC)',
    #         'Volume in Currency (24Hr)',
    #         'Total Volume All Currencies (24Hr)'
    #                 ]])


    #symbol = st.sidebar.text_input('Stock Symbol',value='AAPL',max_chars=5)
    

#if option == 'wallstreetbets':
    #st.subheader('wallstreetbets dashboard logic')

if option == 'stocktwits':
    #st.subheader('chart dashboard logic')
    #symbol= 'AAPL'
    symbol = st.sidebar.selectbox('Stock Symbol', sav_set,index=23,help='Enter Valid Stock Ticker Symbol')
    #symbol = st.sidebar.text_input('Stock Symbol',value='AAPL',max_chars=5,help='Enter Valid Stock Ticker Symbol')
    r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json")
    data = r.json()
    
    #print(data)
    col1, mid, col2 = st.columns([1,1,10])
    with col1:
        st.image('stocktwits-logomark-black.png',width=100)
    with col2:
        st.header('Stockwits - '+symbol)

    if data['response']['status'] == 404:
         st.write(f'{symbol} not available!')
        
    else:    
        st.write('Showing '+str(len(data['messages']))+f' most recent posts shared by Stocktwits community on {symbol}.')
        st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

        for message in data['messages']:
            col1, col2 = st.columns([2,10])
            with col1:
                st.image(message['user']['avatar_url'],width=60)
            with col2:
                st.write(message['user']['username'])
                st.write('Published: '+message['created_at'])
            
            st.write(message['body'])
            st.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
            #st.write('_______________________________________________________________')

    #st.write(data)

st.sidebar.write('Made by Ng Zhili - 2021')
st.sidebar.write("View source code [here](https://github.com/ngzhili/financial-dashboard)")

#df = pd.DataFrame(
    #np.random.randn(50, 20),
    #columns=('col %d' % i for i in range(20)))

#st.dataframe(df)  # Same as st.write(df)

#st.image('https://www.nasdaq.com/sites/acquia.prod/files/styles/720x400/public/image/fad5aa82561887202560b4dba338bef2a56751e6_742299cbdba5f731f487c3c190f8cee5.png?itok=BuSFq0hp')


# Run Application
# streamlit run stock-dashboard.py