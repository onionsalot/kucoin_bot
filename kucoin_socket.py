import asyncio
from pynput.keyboard import Key, Listener
from pynput import keyboard
import logging
import os 
import threading
from kucoin.client import Client
from kucoin.asyncio import KucoinSocketManager
import timetest

api_key = '60a0758a365ac600068a290b'
api_secret = 'd88a265a-86e4-45e1-8347-7263b8940f97'
api_passphrase = '123poi123'
looper = {'loop':True}
def on_press(key):
    pass

def on_release(key):
    if key == Key.esc:
        # Stop listener
        print('Close Kucoin and Pynput connection')
        looper['loop'] = False
        return False

# Collect events until released
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()



async def main():
    global loop

    # callback function that receives messages from the socket
    async def handle_evt(msg):
        if looper['loop'] == False:
            await ksm.unsubscribe('/market/ticker:ETH-USDT')

        if msg['topic'] == '/market/ticker:ETH-USDT':
            # print(f'got ETH-USDT tick:{msg["data"]}', end='\r')
            print(f'{timetest.current_time()}got ETH-USDT tick:{msg["data"]["price"]}', end='\r', flush=True)


    client = Client(api_key, api_secret, api_passphrase)

    ksm = await KucoinSocketManager.create(loop, client, handle_evt)

    # for private topics such as '/account/balance' pass private=True
    ksm_private = await KucoinSocketManager.create(loop, client, handle_evt, private=True)

    # Note: try these one at a time, if all are on you will see a lot of output
    print('looptest')
    # ETH-USDT Market Ticker
    await ksm.subscribe('/market/ticker:ETH-USDT')
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
    while looper:
        print("sleeping to keep loop open")
        await asyncio.sleep(20, loop=loop)


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())