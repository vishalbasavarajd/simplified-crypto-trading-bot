from flask import Flask, request, render_template_string
import logging
from bot import BasicBot
from config import LOG_FILE, DEFAULT_SYMBOL

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

bot = BasicBot(mock=True)
app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Binance Futures Trading Bot</title>
    <style>
        body {
            background-color: #0b0e11;
            color: #eaecef;
            font-family: Arial, sans-serif;
        }
        .container {
            display: flex;
            gap: 30px;
            max-width: 1000px;
            margin: 40px auto;
        }
        .card {
            background: #161a1e;
            padding: 25px;
            border-radius: 10px;
            width: 50%;
        }
        h2 {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-top: 12px;
            font-size: 14px;
        }
        input, select {
            width: 100%;
            padding: 8px;
            margin-top: 6px;
            border-radius: 5px;
            border: none;
            background: #0b0e11;
            color: white;
        }
        .btn-group {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }
        button {
            flex: 1;
            padding: 10px;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            cursor: pointer;
        }
        .buy {
            background: #0ecb81;
            color: black;
        }
        .sell {
            background: #f6465d;
            color: white;
        }
        pre {
            background: #0b0e11;
            padding: 15px;
            border-radius: 6px;
            overflow-x: auto;
        }
        .label {
            color: #848e9c;
            font-size: 13px;
        }
    </style>
</head>
<body>

<div class="container">

    <!-- PLACE ORDER -->
    <div class="card">
        <h2>Place Order</h2>
        <form method="post">
            <label>Trading Pair</label>
            <input name="symbol" value="{{symbol}}" readonly>

            <label>Side</label>
            <select name="side">
                <option value="BUY">BUY</option>
                <option value="SELL">SELL</option>
            </select>

            <label>Order Type</label>
            <select name="order_type">
                <option value="MARKET">MARKET</option>
                <option value="LIMIT">LIMIT</option>
                <option value="STOP">STOP-LIMIT</option>
            </select>

            <label>Quantity</label>
            <input name="quantity" step="0.001" required>

            <label>Price (for LIMIT / STOP)</label>
            <input name="price" step="0.1">

            <label>Stop Price (STOP-LIMIT only)</label>
            <input name="stop_price" step="0.1">

            <div class="btn-group">
                <button class="buy" type="submit" name="action" value="BUY">Buy</button>
                <button class="sell" type="submit" name="action" value="SELL">Sell</button>
            </div>
        </form>
    </div>

    <!-- ORDER SUMMARY -->
    <div class="card">
        <h2>Order Summary</h2>

        {% if response %}
            <p><span class="label">Order ID:</span> {{ response.orderId }}</p>
            <p><span class="label">Symbol:</span> {{ response.symbol }}</p>
            <p><span class="label">Side:</span> {{ response.side }}</p>
            <p><span class="label">Type:</span> {{ response.type }}</p>
            <p><span class="label">Quantity:</span> {{ response.quantity }}</p>
            <p><span class="label">Status:</span> {{ response.status }}</p>

            <h4>Raw Response</h4>
            <pre>{{ response | tojson(indent=2) }}</pre>
        {% else %}
            <p class="label">No order placed yet.</p>
        {% endif %}
    </div>

</div>

<p style="text-align:center;color:#848e9c">
    Binance Futures Trading Bot • Flask Backend • Mock Mode
</p>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    response = None

    if request.method == "POST":
        symbol = request.form["symbol"]
        side = request.form["action"]
        order_type = request.form["order_type"]
        quantity = float(request.form["quantity"])

        if order_type == "MARKET":
            response = bot.market_order(symbol, side, quantity)

        elif order_type == "LIMIT":
            price = float(request.form["price"])
            response = bot.limit_order(symbol, side, quantity, price)

        elif order_type == "STOP":
            price = float(request.form["price"])
            stop_price = float(request.form["stop_price"])
            response = bot.stop_limit_order(symbol, side, quantity, stop_price, price)

    return render_template_string(HTML, response=response, symbol=DEFAULT_SYMBOL)

if __name__ == "__main__":
    print("🚀 Flask running at http://127.0.0.1:5000")
    app.run(debug=True)
