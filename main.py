import click
import time
import base64
import hmac
import requests
import hashlib
import datetime
from kucoin.client import Client
import time_display
import json





with open('config.json') as file:
    config = json.load(file)


def main():
    # //=== V A R   S E T U P ===//
    api_key = config['api_key']
    api_secret = config['api_secret']
    api_passphrase = config['api_passphrase']
    mode = config['fetch_mode']
    pairing = config['pairing']
    take_profit = int(config['take_profit_percentage'])
    buy_percentage = int(config['amount_to_use_percentage'])
    discord_token = config['discord_token']
    discord_channel = config['discord_channel']

    # //=== S E T U P   C L I E N T ===//
    url = 'https://openapi-sandbox.kucoin.com/api/v1/accounts'
    client = Client(api_key, api_secret, api_passphrase, {"verify": False, "timeout": 20})

    for account in client.get_accounts():
        if account['type'] == 'main' and account['currency'] == pairing:
            main = account
        elif account['type'] == 'trade' and account['currency'] == pairing:
            trade = account

    buy_percentage_amount = "{:.2f}".format(float((trade['balance'])) * (buy_percentage/100))

    print(f"""
    {time_display.current_time()}Main account: {main['balance']}
    {time_display.current_time()}Trade account: {trade['balance']}
    
    {time_display.current_time()}Using {buy_percentage}% of {trade['balance']} {pairing}:  {buy_percentage_amount}
    """)

    # // === S E T U P   M A R K E T   D I C T === //
    ticker_list = ()
    markets = client.get_symbols()
    for item in markets:
        if item['quoteCurrency'] == 'USDT' and item['enableTrading'] == True:
            ticker_list = ticker_list + (item['baseCurrency'],)
    
    print(ticker_list)


    # // === P R O M P T   O R   S C R A P E === //
    coin_input = input('Please enter coin (example: BTC): ')
    while coin_input not in ticker_list:
            coin_input = input('COIN NOT FOUND.... Try again: ')

    success = False
    while success == False:
        try: 
            order_id = client.create_market_order('ETH-USDT', Client.SIDE_BUY, funds=buy_percentage_amount)
            if bool(order_id):
                success = True
        except Exception:
            print('rip')
            
        

    # order_id = client.create_market_order('UUSUD-USDT', Client.SIDE_BUY, funds=buy_percentage_amount)
    order =  client.get_order(order_id['orderId'])
    order_summary = f"""
    {time_display.current_time()}ORDER_ID: {order['id']}
    {time_display.current_time()}Pairing: {order['symbol']}
    {time_display.current_time()}Amount used(USDT): {order['dealFunds']}
    {time_display.current_time()}Amount bought({coin_input}): {order['dealSize']}
    {time_display.current_time()}Order placed @ {datetime.datetime.fromtimestamp(order['createdAt']/1000).strftime('%Y-%m-%d %H:%M:%S.%f')}


    """
    print(order_summary)
