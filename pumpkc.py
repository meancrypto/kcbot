from kucoin.client import Client as kClient
import time

api_key = ""
api_secret = ""
api_passphrase = ""
xclient = kClient(api_key, api_secret, api_passphrase)
allCoins = []

def fn(value,precision):
    return format(value,"."+str(precision)+"f")

class pumpConfig:
    buyAmount = 2       # $ Value to spend. BTC amount will be determined if BTC pair
    buyAt = 1.01        # Multiplier of base price
    sellAt = 1.6        # Multiplier of base price  
    currency = "USDT"   # Currency to use when buying pair

    def __init__(self,test=False):
        if test == False:
            self.buyAmount = self.getAmount()
            self.currency = self.getCurrency()
            self.buyAt = self.getMultiplier('buy')
            self.sellAt = self.getMultiplier('sell')
    
    def getAmount(self):
        # Retrieves USDT Amount to risk
        # If the pairing is BTC, the USDT amount will be converted to BTC based
        # on current market price
        tval = float(input("How much USDT will you be risking? "))
        return tval

    def getCurrency(self):
        # for pumping Kucoin, the only 2 base currencies used are BTC and USDT
        while True:
            tval = input("What coin pairing? [BTC or USDT]:")
            if tval.upper() in ["BTC","USDT"]:
                return tval.upper()
    
    def getMultiplier(self,tType):
        # A buy and sell price is based on the base price at program start.
        # The buy limit is set as a multiplier x the base price
        tval = float(input(f"What is the multiplier for your {tType} price:"))
        return tval

class kpumpData:
    client = ""
    coin = None
    allCoins = []
    free = 0
    balance = 0
    curPrice = 0
    intialPrice = 0
    buyPrice = 0
    sellPrice = 0
    price = {}
    highPrice = 0
    amount = 0
    pairing = ""
    tradeCount = 0
    currency = ""
    startTime = 0
    HighTime = 0
    orderOpen = True
    buyorderID = 0
    sellorderID = ""
    buyAmount = 0
    buyAt = 1.0
    sellAt = 1.0

    def __init__(self,currency,xclient,buyAt,sellAt,amount,allCoins):
        self.currency = currency
        self.price["buy"] = 0
        self.price["sell"] = 0
        self.client = xclient
        self.buyAt = buyAt
        self.sellAt = sellAt
        self.buyAmount = amount
        self.allCoins = allCoins

        print("Base Currency:" + self.currency)
        print("Risking $" + str(self.buyAmount))
        print("Buying at " + str(self.buyAt) + " and Selling Limit at " +str(self.sellAt))

    def status(self):
        print("Price at Load:" + fn( self.initialPrice, self.precision))        
        print("Order Size:", self.buyQuantity)
        print("Buy at ", fn( self.buyPrice , self.precision))
        print("Sell at" , fn( self.sellPrice , self.precision))
        print("Beginning to pump " + self.coin)        

    def start(self):
        self.pairing = self.coin + "-" + self.currency
        self.precision = self.allCoins[self.pairing]["precision"]     
        self.buyAmount = self.buyAmount if self.currency=="USDT" else self.buyAmount/float(self.allCoins['BTC-USDT']['price'])
        self.initialPrice = float(self.allCoins[self.pairing]["price"])
        self.curPrice = float(self.allCoins[self.pairing]["price"])
        self.setBuySell()
        self.buyQuantity = round( self.buyAmount / self.buyPrice)
        self.status()

        # send buy Order
        lprint("trying to send buy Order","HEADER")
        try:
            self.buyorderID = self.order("BUY")
            print('buyOrder goes here')
        except Exception as e:
            print("Buy failed with exception:")
            print(e)
            print("Continuing anyway...let's see what happened")            

    def setBuySell(self):
        self.buyPrice = round( self.initialPrice* self.buyAt , 8)
        self.sellPrice = round( self.initialPrice * self.sellAt , 8)

    def order(self,myside,stype="limit"):
        try:
            precision = self.precision
            if myside == "BUY":
                side = self.client.SIDE_BUY
                price = self.buyPrice
                quantity = self.buyQuantity
            elif myside == "SELL":
                side = self.client.SIDE_SELL
                price = self.sellPrice
                quantity = self.free

            
            sPrice = format(price,"."+str(precision)+"f")
            
            if stype == "limit":
                order = self.client.create_limit_order(
                    self.pairing,
                    side,
                    sPrice,
                    quantity) 
                lprint("{} Order for {} of {} at {} {}".format(side, quantity, self.coin, price, self.currency))

            elif stype == "market":
                order = self.client.create_market_order(
                    self.pairing,
                    side,
                    quantity)
                lprint(f"Market Order for {quantity} {self.coin}")

            return order["orderId"]  
        except Exception as e:
            print("Exception in pumpData.order")
            print(e)

    def cancel_order(self,id=None):
        if id is None:
            id = self.buyorderID
        print(f"Trying to cancel order {id}")
        try:    
            self.client.cancel_order(id)
            print("Canceled order")
        except:
            print("Unable to cancel order")
    
    def getAccountInfo(self):
        accountInfo = self.client.get_accounts()
        for i in accountInfo:
            if i["currency"] == self.coin and i["type"] == "trade":
                self.free = float(i["available"])
                self.balance = float(i["balance"])
                break
        print(f"You have {self.free} {self.coin} avaiable.\n")

    def getCoin(self):
        while self.coin == None:
            tVal = input("Enter the name for your token: [enter to exit]")
            tVal = tVal.upper()
            if tVal == "":
                exit()
            if tVal.upper() + "-" + self.currency in self.allCoins:
                self.coin = tVal.upper()
            else:
                print("Invalid coin name")

    def pumpOptions(self):
        exit = False
        while exit == False:
            print("1. Get Current Account Info")
            print(f"2. Market Order {self.free} {self.coin}")
            print(f"3. Limit Order {self.free} {self.coin}")
            print("X. Exit")
            tVal = input("Choose an option:")
            if tVal.upper() == "X":
                return None
            elif tVal == "1":
                self.getAccountInfo()
            elif tVal == "2":
                if self.free > 0:
                    myorder = self.order("SELL",stype="market")
                else:
                    print(f"No {self.coin} available")
            elif tVal == "3":
                if self.free > 0:
                    myorder = self.order("SELL",stype="limit")
                else:
                    print(f"No {self.coin} available")


def getValues(client):
    # retrieve all symbols from Exchange
    # returns all pairings as a list of
    # dictionaries with { pairing: xx , precision: xx}
    # necessary for determining precision of decimals in trade 
    coins = {}
    coinData = {}
    prices = client.get_ticker()['ticker']
    for i in prices:
        coinData[i["symbol"]] = i["last"] 
    symbols = client.get_symbols()
    for i in symbols:
        precision = len(i["priceIncrement"]) - 2
        coins[i["symbol"]] = { "name" : i["name"],"precision":precision, "price":coinData[i["symbol"]] }
    return coins        

def lprint(content,style="HEADER"):
    bcolors = {
        'HEADER' : '\033[95m',
        'OKBLUE' : '\033[94m',
        'OKCYAN' : '\033[96m',
        'OKGREEN' : '\033[92m',
        'WARNING' : '\033[93m',
        'FAIL' : '\033[91m',
        'ENDC' : '\033[0m',
        'BOLD' : '\033[1m',
        'UNDERLINE' : '\033[4m',
    }
    prefix = bcolors[style]
    print(prefix + str(content) + bcolors["ENDC"])    
    return None

print("===")
print("Kucoin Pump Buyer")
pconfig = pumpConfig()
lprint("Loading coin listings...","HEADER")        
allCoins= getValues(xclient)  
lprint(f"{len(allCoins)} Coin Pairings loaded","HEADER")    

pump = kpumpData(pconfig.currency , xclient , pconfig.buyAt , pconfig.sellAt , pconfig.buyAmount , allCoins)
pump.getCoin()
pump.start()
pump.pumpOptions()

