import streamlit as st
import yfinance as yf
import pandas as pd
import datetime as dt
import plotlyGraphs

stock_symbols = []
with open('S&P500Symbols.txt') as sp:
    securities = sp.readlines()
    for s in securities:
        stock_symbols.append(s.strip())
st.write("""# Explore Stocks in the S&P 500""")

sp500 = yf.Ticker('^GSPC')

sp500_start,sp500_end = st.select_slider('Slide me to see the opening and closing prices for the S&P 500 ', options= list(pd.date_range(dt.date(1927, 12, 30),dt.date.today(),freq='d').date)\
                                ,value = (dt.date(1927, 12, 30),dt.date.today()))

st.line_chart(data = sp500.history(start =sp500_start, end = sp500_end)[['Open','Close']])

st.subheader('Lets look at individual stocks in the S&P 500')
stock_symbol = st.selectbox('Pick a stock from the S&P 500', sorted(stock_symbols))
stock = yf.Ticker(stock_symbol)
stock_info = stock.info
stock_history = stock.history(period = 'max')
stock_i_holders = stock.institutional_holders

col1, col2 = st.beta_columns(2)
col1.subheader(stock_info['shortName'])
if len(stock_info['longBusinessSummary'].split('.')[0]) < len(stock_info['shortName']) + 1:
    col1.write("""
                  {}.  
    """.format(' '.join(stock_info['longBusinessSummary'].split('.')[0:2])))
else:
    col1.write("""
                  {}.  
    """.format(stock_info['longBusinessSummary'].split('.')[0]))
# pd.DataFrame(stock_info)
col1.table(pd.DataFrame({'Sector':stock_info['sector'],'State':stock_info['state'],\
                             'Current Price': '$ '+ str(stock_info['regularMarketPrice'])}, index =[stock_symbol]).assign(hack='').set_index('hack'))

col2.subheader('Choose a date range')
start_date = col2.date_input('Start date', min_value= stock_history.index.min(), max_value= dt.date.today() - dt.timedelta(1))
end_date = col2.date_input('End date', min_value= stock_history.index.min() + dt.timedelta(1) ,max_value= dt.date.today())

stock_history_df =  stock_history.loc[start_date:end_date]
st.dataframe(stock_history_df)

mapper  = {'Long-Term Buy': 3, 'Overweight' : 3, 'Buy' : 2, 'Neutral' : 1,\
 'Hold' : 1, 'Sector Perform' : 1, 'Equal-Weight' : 1, 'Market Perform' : 1,\
 'Sell' : 0,'Outperform' : 3, 'Underperform' : 0,'Underweight' : 0,'Strong Buy' : 3, 'Perform' : 1}

# st.dataframe(stock.recommendations)

recommendation = stock.recommendations['To Grade'].map(mapper).groupby(pd.Grouper(freq="M")).mean()
recom_closingPrice_scatter = plotlyGraphs.two_y_axis_scatter(\
                                x2= recommendation.loc[start_date:end_date].index, y2= recommendation.loc[start_date:end_date].values, \
                                name_2 = '3: Strong Buy | 2: Buy | 1: Hold | 0: Sell', y_title2='Recommendation Scores',\
                                x1= stock_history_df.index, y1= stock_history_df['Close'],\
                                name_1 = 'Closing Price', y_title1='Stock Price ($)',
                                x_title = '', title = 'Recommendations and Stock Closing Prices')

st.plotly_chart(recom_closingPrice_scatter)
st.write("""Recommendations are analyst recommendations from yahoo finance. The recommendation scores are the averages for that month. 
Recommendations are from major firms that gives investors a sense for opportunity or safety.
 Change the start and end date above to compare recommendation scores with the stock prices.""")

total_inst_holders = pd.read_csv('institutional_holders.csv')
total_inst_holders = total_inst_holders.groupby('Holder')['Value'].sum()


st.plotly_chart(plotlyGraphs.stacked_barplot(stock_i_holders,total_inst_holders,stock_symbol,'How much did institutions spend on the S&P 500?','Value ($)'))
st.write("""The red represents the total value the institution invested in the individual stock.  
The blue represents the total value the institution has invested in the S&P 500.  
            **Note:** the red can be hard to see. 
            An institution may invest 1 trillion in the S&P500, but only 1 billion in a specific stock.
            Zoom in to see visualize the differences.
            """)
col1, col2 = st.beta_columns([.3,1])

st_radio = col1.radio('', ['All','Min','Max','Median'])
col2.subheader('Stock History Data')
col2.write("""Select the button on the left to get the minimum, middle, or maximum price of {}, or leave as is to see the full price history.""".format(stock_info['shortName']))
if st_radio == 'Max':
    st.dataframe(stock_history[stock_history['Close'] == stock_history['Close'].max()])
elif st_radio == 'Min':
    st.dataframe(stock_history[stock_history['Close'] == stock_history['Close'].min()])
elif st_radio == 'All':
    st.dataframe(stock_history)
elif st_radio == 'Median':
    st.dataframe(stock_history[stock_history['Close'] == stock_history['Close'].median()])

#footer
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb


def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="black",
        text_align="center",
        height="auto",
        opacity=1
    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer():
    myargs = [
        image('https://avatars3.githubusercontent.com/u/45109972?s=400&v=4',
              width=px(25), height=px(25)),
        "Made with streamlit | yfinance | pandas | plotly by ",
        link("https://justsunghwanyoon.blogspot.com/", "Justin S. Yoon"),
        br(), "Source: ",
        link("https://github.com/yoonsunghwan/StreamLitSP500", "github_yoonsunghwan"),
    ]
    layout(*myargs)
footer()