# Simplified Crypto Trading Bot (Binance Futures)

## Overview
This project implements a simplified crypto trading bot using Python and Flask. 
It supports market, limit, and stop-limit orders for USDT-M futures.

## Features
- Market & Limit orders
- Buy & Sell sides
- Stop-Limit order (Bonus)
- Flask-based UI
- Logging of all requests and responses
- Modular & reusable architecture

## Binance Testnet Note
Due to current Binance registration and Testnet access restrictions, a mock execution
layer is used. The mock mode preserves the official Binance Futures Testnet API
request/response structure and can be seamlessly switched to real Testnet credentials
when access is available.

## Tech Stack
- Python
- Flask
- python-binance
- HTML/CSS

## How to Run
```bash
python app.py
