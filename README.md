# kcbot

This project will help you develop a very basic script that will allow you to make purchases to Kucoin.  How and when you use it is up to you, but remember that cryptocurrency investing is highly speculative; just like the stock market, trading tokens is a zero sum game.  Profit is made by some at the expense of others.

In order to use this, you will need an API for Kucoin.  This is a set of private keys that verifies your account with the exchange and allows you to make trades without logging in to their site - your keys replace that process.

You will also need to download Python, a very popular and easy to use programming language.  You will be running your program directly from the source code without the need to compile it, so you have control over the code and can verify that there is no malicious code being used on your computer.  I chose Python because it is an easy to use programming language and can be run from source code.  You can easily look at the program to see that there is no malicious code in it.  Python is slower than many compiled programming languages, but the slowdown here is going to be the human side and how fast/accurately you can typein the name of the token.

Note: You will need to download some packages from PYPI that will help you run the program.

Basic Installation Steps:
1. Download and Install Python (https://www.python.org/downloads/) 
2. From Python, install PIP (Package Installer for Python) if your installation does not include it.
3. Install the modules/libraries that are needed to access the Kucoin API.  I’ve used the Module that is located here: https://pypi.org/project/python-kucoin/ You can install it by going into your command line and typing in “py -m pip install python-kucoin”
4. Get your API keys from Kucoin (https://www.kucoin.com/account/api)
5. Paste your keys into the appropriate spot in your kcbuy.py code.  ***NOTE: DO NOT SHARE YOUR KEYS WITH ANYONE. IF ANYONE ASKS YOU TO SHARE YOUR BOT CODE, DO NOT COPY AND PASTE AND SEND IT TO THEM. DIRECT THEM TO THIS SITE AND LET THEM DOWNLOAD IT ON THEIR OWN***
6. Run your code: python3 kcbuy.py (Mac and Linux)  or py kcbuy.py (Windows).  You should also be able to just double click on kcbuy.py to run the program with the installed Interpreter.

Here’s what the basic program does:
1. Sends a request to Kucoin at program start to download the current price of ALL pairings and stores them for future use.  This is so you can set the price for a Limit Order when the coin is actually announced without having to read current prices.
2. It waits until you enter in the short symbol for your coin (example: DOGE).  This can be upper or lower case
3. The program then calculates how many tokens to buy based on the price you set as a multiplier of the price when the program is started as well as the dollar amount you want to risk.
4. A buy order is sent in based on your parameters
5. At this point, you should switch to your browser so you can monitor progress and handle your buy orders.
6. An option will be given to Market Order sell all of your current tokens.  This will make a quick request to Kucoin to find out how many tokens you have and then will try to sell them.



Special Thanks for this Project go to Sam Hardy for creating the Python Wrapper for this API.
I got all of the code from.  https://python-kucoin.readthedocs.io/en/latest/
If you find it useful, consider donating to him.  He has some tokens he accepts with the address on that page.

An easier method is to tip either of us with BAT using the Brave Browser.   Go here (https://brave.com/brave-rewards/)  to read more about earning BAT from seeing ads and tipping others
