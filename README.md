# Mini Stock Market Simulator 📈

A lightweight full-stack stock trading simulator. This project was built as a focused MVP (Minimum Viable Product) to master asynchronous state synchronization, event-driven UI updates, and real-time backend polling.

---

## The Tech Stack

- **Frontend:** React (TypeScript)
- **Backend:** Python (FastAPI / Django)
- **Database:** PostgreSQL (Ready for production state persistence)

---

## Key Features

- **Dynamic Price Polling:** React triggers an automated background `setInterval` loop to fetch fluctuating stock updates from the Python server every 5 seconds.
- **Event-Driven State UI:** When a user buys or sells a stock, the app instantly bypasses the interval delay to trigger an immediate, manual portfolio and balance refresh—ensuring the data never falls out of sync.
- **Safe Memory Lifecycles:** Implements React `useRef` and explicit `clearTimeout` cleanups to handle overlapping, self-destructing UI transaction notifications safely without memory leaks.
- **Visual State Machine:** The transaction panels and user interface dynamically adjust their layout depending on the chosen context (`buy` vs `sell` states).

---

## Project Structure & Code Highlights

The core engine relies on a single-page unified dashboard handling full-stack network requests and side effects:

- **Asynchronous Lifecycle Guards (`useEffect`):** Manages the initial component mounting payload (fetching active stocks, user balances, and current portfolios) and handles critical browser garbage collection upon unmounting.
- **TypeScript Strict Typing:** Fully typed using standard generic interfaces like `Record<string, number>` to mapping data safely from the API payload.

---

## How to Run Locally

### 1. Backend (Python)
Ensure your FastAPI/Django server is running on local port `8000`:
```bash
# Navigate to your backend directory and start the server
uvicorn main:app --reload
