import React, { useState, useEffect } from 'react';

export default function StockMarket() {
  const [stockName, setStockName] = useState("");
  const [quantity, setQuantity] = useState(1);
  const [message, setMessage] = useState<string>("");
  const [stocks, setStocks] = useState<Record<string, number>>({})
  const [portfolio, setPortfolio] = useState<Record<string, number>>({})
  const [balance, setBalance] = useState<number>(0)
  const [showNotification, setNotification] = useState<boolean>(false)
  const [purchaseState, setPurchaseState] = useState<'buy' | 'sell' | ''>('')
  const timerRef = React.useRef<number | null>(null)

  useEffect(() => {
    const getStocks = async () => {
      const response = await fetch('http://127.0.0.1:8000/stocks');
      const data = await response.json();

      setStocks(data)
    }

    const getBalance = async () => {
      const response = await fetch ('http://127.0.0.1:8000/balance')
      const data = await response.json()

      setBalance(Number(data))
    }

    const getPortfolio = async () => {
      const response = await fetch ('http://127.0.0.1:8000/portfolio')
      const data = await response.json()

      setPortfolio(data)
    }

    const intervalID = setInterval(getStocks, 5000)

    getStocks()
    getBalance()
    getPortfolio()

    return () => clearInterval(intervalID)

  }, [])
  
  const updatePortfolio = async () => {
      const response = await fetch ('http://127.0.0.1:8000/portfolio')
      const data = await response.json()

      setPortfolio(data)
  }

  const buyStocks = async () => {
    const response = await fetch('http://127.0.0.1:8000/buy', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json'},
      body: JSON.stringify({stockName: stockName, quantity: quantity})
    })
    if (response.ok) {
      const mes = await response.json()
      setBalance(mes.balance)
      setMessage(mes['status'])

      if (timerRef.current) {
        clearTimeout(timerRef.current)
      }

      setNotification(true)

      updatePortfolio()

      timerRef.current = setTimeout(() => setNotification(false), 3000)
    }
  }

  const sellStocks = async () => {
    const response = await fetch('http://127.0.0.1:8000/sell', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json'},
      body: JSON.stringify({stockName: stockName, quantity: quantity})
    })

    if (response.ok) {
      const mes = await response.json()
      setBalance(mes.balance)
      setMessage(mes['status'])

      if (timerRef.current) {
        clearTimeout(timerRef.current)
      }

      setNotification(true)

      updatePortfolio()

      timerRef.current = setTimeout(() => setNotification(false), 3000)
    }
  }


  return (
      <div style={{ backgroundColor: '#121212', color: 'white', minHeight: '100vh', padding: '20px' }}>
          <h1 style={{ color: 'white' }}>Stock Trading Simulator</h1>

          <ol>
            {Object.entries(stocks).map(([stockName, price]) => (

            <React.Fragment key={stockName}>

            <li className="border-b py-2">
              <strong>{stockName}</strong>: ${price.toFixed(2)}
            </li> 

            <button onClick={() => setStockName(stockName)}>
                Choose {stockName}
            </button> 

            </React.Fragment>

          ))}
          </ol>
          {stockName && <div>
              <button onClick={() => setPurchaseState('buy')}>
                buy
              </button>

              <button onClick={() => setPurchaseState('sell')}>
                sell
              </button>
              
          </div>}

          <div key='portfolio'>
            <h3>
              Portfolio
            </h3>

            <ul>
            {Object.entries(portfolio).map(([stockName, numOfShares]) => (
              <li key={stockName}>
                <strong>{stockName}</strong>: <p>{numOfShares}</p>
              </li>
            ))}
            </ul>

          </div>
          
          {purchaseState === 'buy' && 
          <div>
          <p>You have selected: {stockName}</p>
              
              <p>Select quantity: <input type='number' min='1' value={quantity} onChange={(e) => setQuantity(Number(e.target.value))}></input> </p>

              <p>Estimated Cost: ${(stocks[stockName] * quantity).toFixed(2)}</p>

              <button onClick={buyStocks}>Buy Stocks</button>
          </div>
          }

          {purchaseState === 'sell' && 
          <div>
          <p>You have selected: {stockName}</p>
              
              <p>Select quantity: <input type='number' min='1' value={quantity} onChange={(e) => setQuantity(Number(e.target.value))}></input> </p>

              <p>Estimated Price: ${(stocks[stockName] * quantity).toFixed(2)}</p>

              <button onClick={sellStocks}>Sell Stocks</button>
          </div>
          }

          {showNotification && <p>Transaction Status: {message}</p>}

          <p>Your Balance: {balance}</p>
      </div>
  );
}