# newHighLow
This scanner will tell you in a telegram channel or group when BTC or ETH are breaking new highs and lows.

pip3 install telegram-send

pip3 install python-binance

Run ethOD.py for eth new highs and lows
Run btcOD.py for btc new highs and lows

Make sure to setup apiHighs.py with your api keys that you aquire from binance.

SETTING UP TELEGRAM

Go to @BotFather on telegram and setup an Bot with the easy to follow instructions.

Alternatively please use in the cli

telegram-send --configure

remove the conf = "user1.conf" from the telegram-send() portion of the code
