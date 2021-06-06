import asyncio
from pynput.keyboard import Key, Listener
from pynput import keyboard
import logging
import os 
import threading
from kucoin.client import Client
from kucoin.asyncio import KucoinSocketManager
import time_display
import json


async def main(loop, order, bought_price):
    with open('config.json') as file:
        config = json.load(file)

    api_key = config['api_key']
    api_secret = config['api_secret']
    api_passphrase = config['api_passphrase']

    def new_sell(client, sell_price, sell_size):
        res = client.cancel_all_orders( "" )
        print('Orders cancelled: ', res, sell_price, sell_size)
        while True:
            order = client.create_limit_order("BTC-USDT", Client.SIDE_SELL, sell_price, sell_size)
            if len(order) == 0:
                print('Sell Failed... retrying...')
            else:
                break
        return order

    looper = {'loop':True}
    def on_press(key):
        pass

    def on_release(key):
        if key == Key.esc:
            # Stop listener
            looper['loop'] = False
            print('Close Kucoin and Pynput connection')
            return False
        
        if key == Key.tab:
            sell_order = new_sell(client, int(float(bought_price) + (float(bought_price) * 3)), order['dealSize'])


    # Collect events until released
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    # callback function that receives messages from the socket
    async def handle_evt(msg):
        if looper['loop'] == False:
            await ksm.unsubscribe('/market/ticker:BTC-USDT')
            return

        if msg['topic'] == '/market/ticker:BTC-USDT':
            # print(f'got ETH-USDT tick:{msg["data"]}', end='\r')
            print(f'{time_display.current_time()} Current price of BTC-USDT: ( {time_display.current_percent(bought_price, msg["data"]["price"])} % ) {msg["data"]["price"]}', end='\r', flush=True)


    client = Client(api_key, api_secret, api_passphrase)

    ksm = await KucoinSocketManager.create(loop, client, handle_evt)

    # for private topics such as '/account/balance' pass private=True
    ksm_private = await KucoinSocketManager.create(loop, client, handle_evt, private=True)

    # Note: try these one at a time, if all are on you will see a lot of output
    print('looptest')
    # ETH-USDT Market Ticker
    await ksm.subscribe('/market/ticker:BTC-USDT')
    # await ksm.unsubscribe('/market/ticker:ETH-USDT')
    # BTC Symbol Snapshots
    # await ksm.subscribe('/market/snapshot:BTC')
    # # KCS-BTC Market Snapshots
    # await ksm.subscribe('/market/snapshot:KCS-BTC')
    # # All tickers
    # await ksm.subscribe('/market/ticker:all')
    # # Level 2 Market Data
    # await ksm.subscribe('/market/level2:KCS-BTC')
    # # Market Execution Data
    # await ksm.subscribe('/market/match:BTC-USDT')
    # # Level 3 market data
    # await ksm.subscribe('/market/level3:BTC-USDT')
    # # Account balance - must be authenticated
    # await ksm_private.subscribe('/account/balance')
    print('return from subscribe')
    while looper:
        if looper['loop'] == False:
            print('bloop')
            return
        await asyncio.sleep(1, loop=loop)


def print_loop(order, bought_price):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(main(loop, order, bought_price), return_exceptions=False))
