import yfinance as yf
import pandas as pd
from datetime import datetime
import os

def fetch_gold_price():
    # Fetch today's data for gold futures (GC=F)
    ticker = "GC=F"
    data = yf.download(ticker, period="1d", interval="1d")
    
    if not data.empty:
        # Add date and format
        data.reset_index(inplace=True)
        data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
        
        # Keep only relevant columns
        data = data[['Date', 'Close']]
        
        # Append to CSV if not weekend
        if datetime.today().weekday() < 5:  # 0=Mon, 4=Fri
            file_path = "data/gold_prices.csv"
            if not os.path.exists(file_path):
                data.to_csv(file_path, index=False)
            else:
                data.to_csv(file_path, mode='a', header=False, index=False)
            print(f"Data updated for {data['Date'].iloc[0]}")
        else:
            print("Skipping weekend update.")
    else:
        print("No data fetched.")

if __name__ == "__main__":
    fetch_gold_price()