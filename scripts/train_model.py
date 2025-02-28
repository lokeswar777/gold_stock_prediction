import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import joblib
from datetime import datetime
import os

def train_model():
    # Load historical data
    df = pd.read_csv("data/gold_prices.csv")
    
    if len(df) < 8:
        print("Not enough data to train model.")
        return
    
    # Feature engineering: Use past 7 days to predict next day
    window_size = 7
    X, y = [], []
    for i in range(window_size, len(df)):
        X.append(df['Close'].iloc[i-window_size:i].values)
        y.append(df['Close'].iloc[i])
    
    # Split data
    split = int(0.8 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Model updated. MAE: ${mae:.2f}")
    
    # Save model
    joblib.dump(model, "models/gold_price_model.pkl")

if __name__ == "__main__":
    if datetime.today().weekday() < 5:  # Only train on weekdays
        train_model()
    else:
        print("Skipping weekend training.")