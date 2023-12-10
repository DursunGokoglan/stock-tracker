import requests
import credentials
from twilio.rest import Client
import datetime as dt
import random

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "ARM",
    "apikey": credentials.STOCK_API_KEY
}

stock_response = requests.get("https://www.alphavantage.co/query", params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()

news_parameters = {
    "q": "arm+semiconductor",
    "apiKey": credentials.NEWS_API_KEY
}

news_response = requests.get("https://newsapi.org/v2/everything?", params=news_parameters)
news_response.raise_for_status()
news_data = news_response.json()

current_day = dt.datetime.now().day
current_month = dt.datetime.now().month
current_year = dt.datetime.now().year

if current_day <= 10:
    one_day_before_close = float(stock_data['Time Series (Daily)'][f"{current_year}-{current_month}-0{current_day - 2}"]['4. close'])
    two_day_before_close = float(stock_data['Time Series (Daily)'][f"{current_year}-{current_month}-0{current_day - 3}"]['4. close'])
elif current_day == 11:
    one_day_before_close = float(stock_data['Time Series (Daily)'][f"{current_year}-{current_month}-{current_day - 2}"]['4. close'])
    two_day_before_close = float(stock_data['Time Series (Daily)'][f"{current_year}-{current_month}-0{current_day - 3}"]['4. close'])
else:
    one_day_before_close = float(stock_data['Time Series (Daily)'][f"{current_year}-{current_month}-{current_day - 2}"]['4. close'])
    two_day_before_close = float(stock_data['Time Series (Daily)'][f"{current_year}-{current_month}-{current_day - 3}"]['4. close'])

daily_change = round(((one_day_before_close - two_day_before_close) / two_day_before_close * 100), 2)

random_article = random.choice(news_data["articles"])["description"].split(".")[0]

client = Client(credentials.TW_ACCOUNT_SID, credentials.TW_AUTH_TOKEN)
message = client.messages.create(body=f"{stock_parameters["symbol"]} change yesterday: {daily_change}% ; {random_article}", from_="+12243026830", to="+905061347436")
