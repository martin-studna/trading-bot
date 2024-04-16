from argparse import ArgumentParser, Namespace
import configparser

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pytrading212 import EquityOrder
from pytrading212 import Equity
from pytrading212 import Mode
from pytrading212 import OrderType
from pytrading212 import MarketOrder

def main(args: Namespace):
    
    config = configparser.ConfigParser()
    config.read('../config.ini')

    driver = webdriver.Chrome(service=Service())
    equity = Equity(email=config['ACCOUNT']['email'], password=config['ACCOUNT']['password'], driver=driver, mode=Mode.DEMO)
    
    # Valid order
    order = EquityOrder(instrument_code="AAPL_US_EQ", order_type=OrderType.MARKET, quantity=2)
    # Check order validity
    if equity.check_order(order)[0]:
        # Review order
        print(equity.review_order(order))
        # Execute order
        print(equity.execute_order(order))
        
    market_order = MarketOrder(instrument_code="AAPL_US_EQ", quantity=1)
    
    if equity.check_order(market_order)[0]:
        # Review order
        print(equity.review_order(market_order))
        # Execute order
        print(equity.execute_order(market_order))

if __name__ == "__main__":
    parser = ArgumentParser()
    args = parser.parse_args()
    main(args)