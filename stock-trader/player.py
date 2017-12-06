#!/bin/python
# Stock Trader, by Matthew Schieber
# Many attempts were made at this. Stock trading is, of course, 
# very hard to predict!  My vanilla attempt involved producing the
# slopes to evaluate the current trend of stocks.  Turns out, the
# zeroth order polynomial model (even more vanilla) is superior!
# This is simply the mean of the current price, for the last 5 days.
# The strategy thereafter is to buy low and sell high.  There are 
# three parameters for my StockTrader class: 1) the percentage above
# the mean price at which to sell a stock. 2) the percentage lower
# than the mean price at which to buy a stock. 3) the fraction of 
# total money to use on a particular investment. After a simple
# search on these parameters, my StockTrader increases its porfolio 
# by more than 4500% on the sample case and nearly 1000% on the test
# case.  This results in a score of 46.0259 on HR, which solves it.
# I really like how the organization of this class turned out!
# template for use on https://www.hackerrank.com/challenges/stockprediction


class StockTrader:
    
    def __init__(self, k, names):
        self.slopes = []
        self.buys = []
        self.sells = []
        self.buy_percent = -3
        self.sell_percent = 3
        self.keep_percent = 2/3
        
        # some hashing is necessary to keep track of stocks
        self.name_map = {}
        for i in range(k):
            self.name_map[names[i]] = i
       
    def printTransactions(self, m, k, d, name, owned, prices):
        
        self.ProduceSlopes(k, name, prices)
        self.CheckBuys(m, k, name, prices)
        self.CheckSells(m, k, owned, prices)
        
        print (len(self.buys) + len(self.sells))
        for i in self.sells:
            print (i[0], " SELL ", i[1]) 
        for i in self.buys:
            print (i[0], " BUY ", i[1])
            
    def ProduceSlopes(self, k, name, prices):
        # collect (current prices - mean = percent change)
        self.slopes = []
        for i in range(k):
            mean = sum(prices[i]) / 5
            self.slopes.append([name[i], (prices[i][4] - mean) / mean * 100])
        self.slopes = sorted(self.slopes, key=lambda x: x[1])
            
    def CheckBuys(self, m, k, name, prices):
        # if the current price is less than self.buy_percent higher than the mean, sell it
        # keep at least self.keep_percent cash in reserves
        for i in range(k):
            c = 0
            n = self.slopes[i][0]
            v = self.slopes[i][1]
            index = self.name_map[n]
            if(v < self.buy_percent):
                while(c * float(prices[index][4]) < m * self.keep_percent): c += 1
                if (c - 1 > 0):
                    m -= (c - 1) * float(prices[index][4])
                    self.buys.append([n, c - 1])
        
    def CheckSells(self, m, k, owned, prices):
        # if the current price is more than self.sell_percent higher than the mean, sell it
        for i in range(k):
            n = self.slopes[i][0]
            v = self.slopes[i][1]
            index = self.name_map[n]
            if(owned[index] and (self.sell_percent < v)):
                self.sells.append([n, owned[index]])           
        
    
if __name__ == "__main__": 
    pos = [float(i) for i in input().strip().split()] 
    m = pos[0]
    k = int(pos[1])
    d = int(pos[2])
    
    name = []
    owned = []
    prices = []
    
    for i in range(k):
        c = ''
        named = False
        ownedd = False
        prices.append([])
        for j in input():
            if(j != ' '):
                c += j
            else:
                if(not named):
                    name.append(c)
                    named = True
                    c = ''
                elif(not ownedd):
                    owned.append(int(c))
                    ownedd = True
                    c = ''
                else:
                    prices[i].append(float(c))
                    c = ''
        prices[i].append(float(c))
    
    Trader = StockTrader(k, name)
    Trader.printTransactions(m, k, d, name, owned, prices)

