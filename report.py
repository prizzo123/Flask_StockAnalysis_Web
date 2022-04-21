from time import sleep
import numpy as np
import pandas as pd
import math
from bs4 import BeautifulSoup
import requests
import datetime
from dateutil import parser
from requests.models import DecodeError
import yfinance
import yahoo_fin.stock_info as si
import talib
from datetime import datetime as dt, timedelta
import os
import sys

#earningDates = []

def scrape_earnings_date(ticker):
    # define URL
    curr_url = 'https://finance.yahoo.com/quote/' + ticker
    # send a GET request and check if the request is successful
    response = requests.get(curr_url)
    if response.status_code != 200:
        print('Failure')

    # Parse raw data
    try:
        results = BeautifulSoup(response.content, 'lxml')
        earnings_date = results.find('span', {"data-reactid":"158"})
        earnings_date = earnings_date.get_text()
    except:
        return('cannot gather data')

    return(earnings_date)

def macro_rsi(ticker):
    try:
        #stockData = yfinance.download(ticker,start,end)
        yfinanceTicker = yfinance.Ticker(ticker)
        stockData = yfinanceTicker.history(interval='1d', period="6mo")
        rsi = talib.RSI(stockData["Close"])
        currentRSI = rsi[-1]
        return(currentRSI)
    except ValueError or DecodeError:
        print('cannot compute macroRSI for: ' + str(ticker))

def rsi_calc():
    stocks = []
    earningDates = ""
    f = open('rsi.txt', 'w')
    t = open('ticker.txt', 'w')
    e = open('earningsdate.txt', 'w')
    

    date = dt.now()
    date.day

    f.write('')
    t.write('')
    e.write('')
    f.close()
    t.close()
    e.close()

    start = datetime.datetime.now()-datetime.timedelta(days=365)
    end = datetime.datetime.now()
    hour = datetime.datetime.now()
    hour = hour.time()
    hour = int(hour.strftime("%H"))

    stocks = stocks if len(stocks) > 0 else [
        line.rstrip() for line in open("stocks.txt", "r")]
    for ticker in stocks:
        try:
            macroRSI = macro_rsi(ticker)
            earnings = si.get_next_earnings_date(ticker)
            earningsConv = earnings - date
            earningsConv = earningsConv.days
            if macroRSI <= 30:
                rsi = str(ticker) + ':' + str(macroRSI) + ':' + str(earningsConv) + ':' + "OVERSOLD"
                f = open('rsi.txt', 'a')
                f.write(str(rsi))
                f.write('\n')
                f.close()
            elif macroRSI >= 70:
                rsi = str(ticker) + ':' + str(macroRSI) + ':' + str(earningsConv) + ':' + "OVERBOUGHT"
                f = open('rsi.txt', 'a')
                f.write(str(rsi))
                f.write('\n')
                f.close()
        except:
            print('failed for: ' + str(ticker))

rsi_calc()
