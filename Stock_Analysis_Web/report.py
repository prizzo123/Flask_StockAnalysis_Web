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
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import stockstats
import matplotlib.pyplot as plt

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

def scrape_market_sentiment():
    # define URL
    curr_url = 'https://www.cnbc.com/'
    # send a GET request and check if the request is successful
    response = requests.get(curr_url)
    if response.status_code != 200:
        print('Failure')

    # Parse raw data
    try:
        results = BeautifulSoup(response.text, 'html.parser')
        headline = results.find(class_='MarketsBanner-teaser')
        headline = headline.get_text()
    except:
        return('cannot gather data')

    return(headline)       

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


stocks = []
tickers = []
earningDates = ""
positiveKeywords = []
negativeKeywords = []
imageName = []
n = 0
p = 0
cid = 100

date = dt.now()
date.day

start = datetime.datetime.now()-datetime.timedelta(days=365)
end = datetime.datetime.now()
hour = datetime.datetime.now()
hour = hour.time()
hour = int(hour.strftime("%H"))

stocks = stocks if len(stocks) > 0 else [
    line.rstrip() for line in open("stocks.txt", "r")]

data = scrape_market_sentiment()

positiveKeywords = positiveKeywords if len(positiveKeywords) > 0 else [
    line.rstrip() for line in open("positive_keywords.txt", "r")]

negativeKeywords = negativeKeywords if len(negativeKeywords) > 0 else [
    line.rstrip() for line in open("negative_keywords.txt", "r")]

for substring in negativeKeywords:
    if substring in data:
        n = n + 1
    else:
        print(substring + " Not found!")
for substring in positiveKeywords:
    if substring in data:
        p = p + 1
    else:
        print(substring + " Not found!")

if n > p:
    market_sentiment = "<br> Market Sentiment: low"
elif p > n : 
    market_sentiment = "<br> Market Sentiment: high"

data = '<br>' + '<h2>' + data + '</h2>'

for ticker in stocks:
    try:
        macroRSI = macro_rsi(ticker)
        earnings = si.get_next_earnings_date(ticker)
        earningsConv = earnings - date
        earningsConv = earningsConv.days
        if macroRSI <= 30:
            #dmi(ticker)
            cid = cid + 1
            imageCID = str(cid)
            Name = ticker + ".png"
            imageName.append(Name)
            imageSRC = '<img src=\"' + 'cid: image' + imageCID + '\">'
            earningsDate = '<br>' + '<h3>' + str(ticker) + '</h3>' + imageSRC + '<br>' + 'RSI: ' + str(macroRSI) + '<br>' + 'Days until earnings: ' + str(earningsConv) + '<br>'
            earningDates = earningDates + earningsDate
        elif macroRSI >= 70:
            #dmi(ticker)
            cid = cid + 1
            imageCID = str(cid)
            Name = ticker + ".png"
            imageName.append(Name)
            imageSRC = '<img src=\"' + 'cid: image' + imageCID + '\">'
            earningsDate = '<br>' + '<h3>' + str(ticker) + '</h3>' + imageSRC + '<br>' + 'RSI: ' + str(macroRSI) + '<br>' + 'Days until earnings: ' + str(earningsConv) + '<br>'
            earningDates = earningDates + earningsDate
    except:
        print('failed for: ' + str(ticker))


report_email()   