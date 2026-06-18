from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from random import uniform

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

stocks = {
    'AAPL': 350,
    'NVDA': 1200,
    'GOOG': 450,
    'MSFT': 150,
    'TSLA': 900
}

portfolio = {
    'AAPL': 0,
    'NVDA': 0,
    'GOOG': 0,
    'MSFT': 0,
    'TSLA': 0
}

playerBalance = 10000.00

def fluctuate(stocks_dict):
    for stock, price in stocks_dict.items():
        stocks_dict[stock] = round((price + uniform(-20, 20)), 2)

    return stocks_dict

@app.get("/stocks")
def get_stocks():
    return fluctuate(stocks)

@app.get('/balance')
def get_balance():
    return playerBalance

@app.get('/portfolio')
def get_portfolio():
    return portfolio

@app.post('/sell')
async def process_sell(request: Request):
    global playerBalance

    data = await request.json()

    stockName = data['stockName']
    quantity = data['quantity']

    value = quantity * stocks[stockName]

    if 0 < quantity <= portfolio[stockName]:
        portfolio[stockName] -= quantity

        playerBalance += value

        playerBalance = round(playerBalance, 2)

        return {'status': 'success', 'balance': playerBalance}
    
    return {'status': 'fail', 'balance': playerBalance}


@app.post('/buy')
async def process_buy(request: Request):
    global playerBalance

    data = await request.json()

    stockName = data['stockName']
    quantity = data['quantity']

    total_cost = stocks[stockName] * quantity

    if 0 < total_cost < playerBalance:
        playerBalance -= total_cost

        if stockName in portfolio:
            portfolio[stockName] += quantity
        else:
            portfolio[stockName] = quantity

        playerBalance = round(playerBalance, 2)

        return {'status': 'success', 'balance': playerBalance}
    
    return {'status': 'fail', 'balance': playerBalance}