from flask import Blueprint, render_template
import os

views = Blueprint('views', __name__)

@views.route('/')
def home():
    data = open('C:\\Users\\TehRizz\\Desktop\\Python Projects\\Alpaca\\Flask_StockAnalysis_Web\\Report\\rsi.txt', 'r')
    
    return render_template("home.html", value = data)
