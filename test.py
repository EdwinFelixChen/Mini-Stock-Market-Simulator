import random
from tabulate import tabulate
import sys

stocks = {
    'AAPL': 200,
    'NVDA': 1200,
    'GOOG': 450,
    'MSFT': 150,
    'TSLA': 900
}

def is_valid(item, list, message):
    while True:
            if item in list:
                break
            
            else:
                item = input(message)

    return item

def is_valid_range(item, lower_bound, upper_bound, message):
    while True:
        try:
            item = float(item)

            if lower_bound < item < upper_bound:
                break
            
            else:
                item = input(message)

        except ValueError:
            item = input(message)

    return item

class StockBehaviour:
    def __init__(self, stocks):
        self.stocks = stocks

    def fluctuate(self):
        for stock in self.stocks:
            x = random.randint(1, 10)

            if x <= 5:
                self.stocks[stock] += round(random.uniform(-10, 10), 2)

            elif x <= 7:
                self.stocks[stock] += round(random.uniform(-25, 25), 2)

            elif x <= 9:
                self.stocks[stock] += round(random.uniform(-20, 100), 2)

            else:
                self.stocks[stock] += round(random.uniform(-200, 50), 2)

            if self.stocks[stock] <= 0:
                self.stocks[stock] = 0


    def display(self):
        print(tabulate(self.stocks.items(), ['stock', 'price'], "fancy_grid"))

class Player:
    def __init__(self):
        self.cash = 10000
        self.portfolio = {}
        self.rows = []

    def display_portfolio(self, stocks):
        self.rows = []
        for stock, number in self.portfolio.items():
            value = round(number * stocks[stock], 2)
            number = round(number, 2)
            self.rows.append([stock, number, value])

        print(tabulate(self.rows, ['stock', 'number', 'value'], 'fancy_grid'))

    def update_portfolio(self):
        for stock, number in self.portfolio.copy().items():
            if number < 0.01:
                del self.portfolio[stock]
                

class Game:
    def __init__(self, stocks):
        self.stocks = stocks
        self.running = True
        self.sb = StockBehaviour(stocks)
        self.player = Player()

    def run(self):
        while self.running:
            self.player.update_portfolio()

            try:
                cmd = int(input("1=View, 2=Portfolio, 3=buy, 4=sell, 5=my_cash, 6=quit: "))

            except ValueError:
                print("Please enter a valid command")
                continue

            if cmd == 1:
                self.sb.display()

            elif cmd == 2:
                self.player.display_portfolio(self.stocks)
            
            elif cmd == 3:
                investment = input("Enter the stock and amount (in USD) you would like to invest. Separate by a comma. Ex. NVDA, 1000: ")

                while True:
                    try:
                        stock, value = investment.replace(" ", "").split(",")
                        value = int(value)
                        stock = stock.upper()
                        break

                    except:
                        investment = input("Error. Please enter valid input: ")

                if stock not in self.stocks:
                    print("Error. Stock does not exist")

                elif not 0 < value <= self.player.cash:
                    print("Error. Enter a valid amount to invest")

                else:

                    try: 
                        share_num = round(value / self.stocks[stock], 2)
                        self.player.portfolio[stock] += share_num
                        self.player.cash -= value

                    except KeyError:
                        self.player.portfolio[stock] = share_num
                        self.player.cash -= value

                    except ZeroDivisionError:
                        print("Stock price is zero - cannot buy")
                        continue

                    print("investment success! Would you like to view your portfolio? Press 2")

            elif cmd == 4:
                self.player.display_portfolio(self.stocks)

                if not self.player.portfolio:
                    print("No stocks to sell. Press 3 to buy")
                    continue

                stock = input('Enter the name of the stock you would like to sell: ').strip().upper()

                stock = is_valid(stock, self.stocks, "Invalid. Stock doesn't exist. Please try again: ")

                option = input("Would you like to sell by shares or value? Enter 1 for shares and 2 for value: ")

                option = is_valid(option, ["1", "2"], "Invalid. Please try again: ")

                if option == "1":
                    amount = input(f"Enter the amount of {stock} shares you would like to sell: ")

                    while True:
                        try:
                            amount = float(amount)
                            break

                        except ValueError:
                            amount = input("Please enter a valid number of shares: ")

                elif option == "2":
                    amount = input(f"Enter the amount (in USD) of {stock} you would like to sell: ")

                    while True:
                        try:
                            amount = float(amount)
                            break

                        except ValueError:
                            amount = input("Please enter a valid number of shares: ")

                    amount = amount / self.stocks[stock]

                amount = is_valid_range(amount, 0, self.player.portfolio[stock], "Invalid. Enter a valid amount: ")

                self.player.portfolio[stock] -= amount
                self.player.cash += round(amount * self.stocks[stock], 2)

                print("transaction complete! Thank you for investing with us.")

            elif cmd == 5:
                print(f"Current cash: {self.player.cash}")

            elif cmd == 6:
                self.running = False

            else:
                print("Please enter a valid command!")

            self.sb.fluctuate()
                        

game = Game(stocks)
game.run()