import time
import uuid
import logging

class BasicBot:
    def __init__(self, mock=True):
        self.mock = mock
        logging.info("Mock Binance Futures Bot Initialized")

    def _mock_response(self, symbol, side, order_type, quantity, price=None):
        return {
            "orderId": str(uuid.uuid4()),
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "status": "FILLED",
            "quantity": quantity,
            "price": price,
            "timestamp": int(time.time() * 1000)
        }

    def market_order(self, symbol, side, quantity):
        logging.info(f"Placing MARKET order | {symbol} | {side} | {quantity}")
        return self._mock_response(symbol, side, "MARKET", quantity)

    def limit_order(self, symbol, side, quantity, price):
        logging.info(f"Placing LIMIT order | {symbol} | {side} | {quantity} @ {price}")
        return self._mock_response(symbol, side, "LIMIT", quantity, price)

    def stop_limit_order(self, symbol, side, quantity, stop_price, price):
        logging.info(
            f"Placing STOP-LIMIT order | {symbol} | {side} | {quantity} | stop={stop_price} price={price}"
        )
        response = self._mock_response(symbol, side, "STOP_LIMIT", quantity, price)
        response["stopPrice"] = stop_price
        return response
