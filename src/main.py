from argparse import ArgumentParser, Namespace
import configparser
import alpaca_trade_api as tradeapi
import schedule
import time



# Your Alpaca API key and secret
API_KEY = 'PKTNBBYDWQS81SS48C9X'
API_SECRET = 'cO0l5TiaEVLJO7XlSOClujTrLE8eENNoGWYDLLqO'
BASE_URL = 'https://paper-api.alpaca.markets'  # or use the live URL for real trading

# Initialize the Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# Trading parameters
stock_symbol = 'AAPL'
short_window = 40
long_window = 100

def fetch_data():
    # Fetch historical data for the stock
    # Fetch historical data for the stock
    data = api.get_bars(stock_symbol, tradeapi.TimeFrame.Minute, limit=long_window).df
    return data['close'].tolist()

def moving_average_crossover_strategy():
    prices = fetch_data()
    
    # Calculate moving averages
    short_mavg = sum(prices[-short_window:]) / short_window
    long_mavg = sum(prices) / long_window

    # Check for the crossover
    if short_mavg > long_mavg:
        print("Short MA is above Long MA, BUY signal")
        place_order('buy')
    elif short_mavg < long_mavg:
        print("Short MA is below Long MA, SELL signal")
        place_order('sell')

def place_order(side):
    # Check if there is an existing position
    position_qty = 0
    try:
        position = api.get_position(stock_symbol)
        position_qty = int(position.qty)
    except:
        pass
    
    # Decide order quantity
    order_qty = 10  # Modify as needed

    if side == 'buy' and position_qty <= 0:
        api.submit_order(
            symbol=stock_symbol,
            qty=order_qty,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
    elif side == 'sell' and position_qty > 0:
        api.submit_order(
            symbol=stock_symbol,
            qty=abs(position_qty),  # Close the position
            side='sell',
            type='market',
            time_in_force='gtc'
        )


def main(args: Namespace):
    
    # Schedule the strategy to run every minute
    schedule.every(interval=10).seconds.do(moving_average_crossover_strategy)

    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)
    

if __name__ == "__main__":
    place_order("buy")
    parser = ArgumentParser()
    args = parser.parse_args()
    main(args)