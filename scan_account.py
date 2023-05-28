from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
import config

from class_analysis_technical import TechnicalAnalysis
import yfinance as yf

tc = TradingClient(config.API_KEY, config.SECRET_KEY)

def scanAccount():
    open_positions = tc.get_all_positions()
 
    holding_positions = {}
    for position in open_positions:
        symbol = position.symbol
        holding_price = float(position.avg_entry_price)
        holding_quantity = int(position.qty)     
        
        holding_positions[symbol] = [holding_price, holding_quantity]
        num_positions = len(holding_positions)
    
    available_equity = float(tc.get_account().cash)

    return holding_positions, num_positions, available_equity

def run_ta(holding_positions): 
    
    analysis_result = {}  
    
    for ticker in holding_positions:
        df = yf.download(ticker, start='2022-09-01')
        
        print(f'Running technical analysis on {ticker}...')
        ta = TechnicalAnalysis(df)
        ta.good_to_buy()
        ta.good_to_sell()

        close_price = df['Close'][-1]

        if df['good_to_buy'][-1] == True:
            analysis_result[ticker] = ('Buy', close_price)
        elif df['good_to_sell'][-1] == True:
            analysis_result[ticker] = ('Sell', close_price)
        else:
            analysis_result[ticker] = (None, close_price)
    
    return analysis_result
                        