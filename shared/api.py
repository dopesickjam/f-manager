import requests
import streamlit as st

def get_exchange_rate():
    exchange_request = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key={st.secrets["exchangeratesapi"]["token"]}&symbols=USD,UAH')
    exchange_request = exchange_request.json()
    exchange_date    = exchange_request['date']
    exchange_usd     = exchange_request['rates']['USD']
    exchange_uah     = exchange_request['rates']['UAH']
    uah_to_usd       = exchange_uah / exchange_usd

    return uah_to_usd